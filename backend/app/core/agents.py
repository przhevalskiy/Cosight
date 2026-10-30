"""
CoSight specialist agents — each owns a channel domain, tool subset, and system prompt.

The chat orchestrator routes cross-domain questions; dashboard briefs and section
insights invoke the agent that matches the page channel.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional

NUMERIC_GROUNDING = """
## CRITICAL — Numeric Grounding
You MUST ONLY cite numbers that were returned by a tool call in this conversation
or provided in the user/citation context.
NEVER invent, estimate, or recall figures from memory. If you don't have data,
call the appropriate tool first (when available to you).
"""

BRIEF_GROUNDING = """
Use inline citation markers [1], [2], etc. for EVERY number you mention.
Only cite numbers that appear in the citation list. Do not invent data.
Write 3-5 sentences. No bullet lists. No markdown headers.
"""

SECTION_GROUNDING = """
Write exactly 1–2 plain-language sentences summarizing what happened in ONE dashboard section.
Be specific with numbers from the context only. Do not invent data.
No bullet lists, headers, or citation markers.
"""


@dataclass(frozen=True)
class CosightAgent:
    id: str
    display_name: str
    short_label: str
    domain: str
    tool_names: tuple[str, ...]
    brief_system: str
    section_system: str
    chat_system: str

    def tools_from(self, all_tools: List[dict]) -> List[dict]:
        allowed = set(self.tool_names)
        return [t for t in all_tools if t["name"] in allowed]


_OVERVIEW_BRIEF = (
    "You are the Overview Analyst for CBS Marketing & Communications. "
    "You synthesize web, search, email, and social KPIs into one executive narrative. "
    + BRIEF_GROUNDING
)
_OVERVIEW_SECTION = (
    "You are the Overview Analyst for CBS Marketing & Communications. "
    + SECTION_GROUNDING
)
_ORCHESTRATOR_CHAT = (
    "You are CoSight, the orchestrator for CBS Marketing & Communications. "
    "You coordinate specialist analysts: Web (GA4), Search (GSC), Email (Emma), Social (Sprout), "
    "and Reports. Call only the tools needed for the user's question — prefer the narrowest tool set. "
    "For cross-channel questions, call multiple get_* tools and synthesize. "
    "For report requests, fetch metrics first, then generate_report. "
    + NUMERIC_GROUNDING
    + """
## How to answer
1. Identify which channel(s) the question touches.
2. Call the appropriate tool(s) with the correct date range.
3. Analyze results — trends, prior-period deltas, anomalies.
4. Cite sources (GA4, GSC, Emma, Sprout) with specific numbers.
5. Be concise and executive-ready.

## Date ranges
- "Last 30 days" = today minus 30 days through yesterday
- When the user doesn't specify a range, ask once before calling tools.
"""
)

AGENTS: Dict[str, CosightAgent] = {
    "overview": CosightAgent(
        id="overview",
        display_name="Overview Analyst",
        short_label="Overview",
        domain="Cross-channel marketing performance",
        tool_names=(
            "get_web_metrics",
            "get_seo_metrics",
            "get_email_metrics",
            "get_social_metrics",
        ),
        brief_system=_OVERVIEW_BRIEF,
        section_system=_OVERVIEW_SECTION,
        chat_system=(
            "You are the Overview Analyst — you compare and connect KPIs across GA4, Search Console, "
            "Emma, and Sprout. Lead with the biggest cross-channel story, then support with channel specifics. "
            + NUMERIC_GROUNDING
        ),
    ),
    "web": CosightAgent(
        id="web",
        display_name="Web Analyst",
        short_label="Web",
        domain="Google Analytics 4 website traffic and behavior",
        tool_names=("get_web_metrics",),
        brief_system=(
            "You are the Web Analyst specializing in Google Analytics 4. "
            "Focus on sessions, users, engagement, conversions, and organic traffic. "
            + BRIEF_GROUNDING
        ),
        section_system="You are the Web Analyst (GA4). " + SECTION_GROUNDING,
        chat_system=(
            "You are the Web Analyst — GA4 only. Answer questions about site traffic, user behavior, "
            "conversions, and channel performance. Use get_web_metrics; do not claim email or social figures. "
            + NUMERIC_GROUNDING
        ),
    ),
    "search": CosightAgent(
        id="search",
        display_name="Search Analyst",
        short_label="Search",
        domain="Google Search Console organic visibility",
        tool_names=("get_seo_metrics",),
        brief_system=(
            "You are the Search Analyst specializing in Google Search Console. "
            "Focus on clicks, impressions, CTR, average position, and top queries. "
            "Note GSC's ~3 day reporting lag when relevant. "
            + BRIEF_GROUNDING
        ),
        section_system="You are the Search Analyst (Google Search Console). " + SECTION_GROUNDING,
        chat_system=(
            "You are the Search Analyst — Google Search Console only. Cover rankings, queries, "
            "impressions, and CTR. Use get_seo_metrics exclusively for live numbers. "
            + NUMERIC_GROUNDING
        ),
    ),
    "email": CosightAgent(
        id="email",
        display_name="Email Analyst",
        short_label="Email",
        domain="Emma email marketing campaigns",
        tool_names=("get_email_metrics",),
        brief_system=(
            "You are the Email Analyst specializing in Emma campaign data. "
            "Focus on sends, open rate, click rate, and unsubscribes. "
            + BRIEF_GROUNDING
        ),
        section_system="You are the Email Analyst (Emma). " + SECTION_GROUNDING,
        chat_system=(
            "You are the Email Analyst — Emma only. Discuss campaign engagement and list health. "
            "Use get_email_metrics for all numeric claims. "
            + NUMERIC_GROUNDING
        ),
    ),
    "social": CosightAgent(
        id="social",
        display_name="Social Analyst",
        short_label="Social",
        domain="Sprout Social profiles and content performance",
        tool_names=("get_social_metrics",),
        brief_system=(
            "You are the Social Analyst specializing in Sprout Social. "
            "Focus on impressions, engagements, reach, followers, and platform mix. "
            "Note Sprout excludes the most recent ~2 days when relevant. "
            + BRIEF_GROUNDING
        ),
        section_system="You are the Social Analyst (Sprout Social). " + SECTION_GROUNDING,
        chat_system=(
            "You are the Social Analyst — Sprout Social only. Cover posts, platforms, and audience growth. "
            "Use get_social_metrics for live metrics. "
            + NUMERIC_GROUNDING
        ),
    ),
    "reports": CosightAgent(
        id="reports",
        display_name="Reports Agent",
        short_label="Reports",
        domain="Structured marketing report artifacts and exports",
        tool_names=(
            "get_web_metrics",
            "get_seo_metrics",
            "get_email_metrics",
            "get_social_metrics",
            "generate_report",
        ),
        brief_system=(
            "You are the Reports Agent for CBS MarComm. "
            "Summarize what a stakeholder would need before exporting a formal report. "
            + BRIEF_GROUNDING
        ),
        section_system="You are the Reports Agent. " + SECTION_GROUNDING,
        chat_system=(
            "You are the Reports Agent. Fetch channel metrics with the get_* tools, then assemble "
            "generate_report when the user wants a document. Never skip data fetch before report creation. "
            + NUMERIC_GROUNDING
        ),
    ),
    "chat": CosightAgent(
        id="chat",
        display_name="CoSight Orchestrator",
        short_label="Chat",
        domain="Routes questions to the right channel specialists",
        tool_names=(
            "get_web_metrics",
            "get_seo_metrics",
            "get_email_metrics",
            "get_social_metrics",
            "generate_report",
        ),
        brief_system=_OVERVIEW_BRIEF,
        section_system=_OVERVIEW_SECTION,
        chat_system=_ORCHESTRATOR_CHAT,
    ),
}

CHANNEL_TO_AGENT = {
    "overview": "overview",
    "web": "web",
    "search": "search",
    "seo": "search",
    "email": "email",
    "social": "social",
    "reports": "reports",
}

_ROUTE_PATTERNS: Dict[str, re.Pattern[str]] = {
    "web": re.compile(
        r"\b(web|website|ga4|analytics|pageview|session|bounce|conversion|traffic)\b",
        re.I,
    ),
    "search": re.compile(
        r"\b(seo|search console|gsc|keyword|query|ranking|impression|ctr|position|organic search)\b",
        re.I,
    ),
    "email": re.compile(
        r"\b(email|emma|newsletter|campaign|open rate|click rate|unsubscribe)\b",
        re.I,
    ),
    "social": re.compile(
        r"\b(social|sprout|instagram|facebook|linkedin|twitter|engagement|follower|post)\b",
        re.I,
    ),
    "reports": re.compile(
        r"\b(report|export|pdf|docx|pptx|slide|deck|summary document)\b",
        re.I,
    ),
}


def get_agent(agent_id: str) -> CosightAgent:
    key = CHANNEL_TO_AGENT.get(agent_id, agent_id)
    if key not in AGENTS:
        return AGENTS["chat"]
    return AGENTS[key]


def agent_for_channel(channel: str) -> CosightAgent:
    return get_agent(CHANNEL_TO_AGENT.get(channel, channel))


def resolve_chat_agent(
    message: str,
    scoped_channel: Optional[str] = None,
) -> CosightAgent:
    """Pick a specialist when the question is clearly single-domain; else orchestrator."""
    if scoped_channel:
        mapped = CHANNEL_TO_AGENT.get(scoped_channel)
        if mapped and mapped in AGENTS and mapped not in ("overview", "chat"):
            return AGENTS[mapped]

    scores: Dict[str, int] = {k: 0 for k in ("web", "search", "email", "social", "reports")}
    for key, pattern in _ROUTE_PATTERNS.items():
        if pattern.search(message):
            scores[key] += 1

    best = max(scores.values())
    if best == 0:
        return AGENTS["chat"]

    winners = [k for k, v in scores.items() if v == best]
    if len(winners) == 1:
        return AGENTS[winners[0]]

    return AGENTS["chat"]


def list_agents_public() -> List[dict]:
    """Metadata for UI (sidebar avatars, labels)."""
    return [
        {
            "id": a.id,
            "display_name": a.display_name,
            "short_label": a.short_label,
            "domain": a.domain,
            "tool_names": list(a.tool_names),
        }
        for a in AGENTS.values()
    ]
