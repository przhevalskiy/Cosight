"""
CoSight AI tool definitions — consumed by the agentic chat loop.

Tools are pre-aggregated before entering context to bound token usage.
Numeric grounding invariant: every figure the agent emits must trace to a
tool result — the system prompt forbids citing any number not returned by a tool.
"""
from __future__ import annotations

COSIGHT_TOOLS = [
    {
        "name": "get_web_metrics",
        "description": (
            "Fetch Google Analytics 4 web metrics for a date range. "
            "Returns sessions, pageviews, active users, bounce rate, conversions, "
            "avg session duration, organic sessions, and daily timeseries. "
            "Use this for any question about website traffic, user behavior, or "
            "organic search channel performance."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "Start date in YYYY-MM-DD format",
                },
                "end_date": {
                    "type": "string",
                    "description": "End date in YYYY-MM-DD format",
                },
            },
            "required": ["start_date", "end_date"],
        },
    },
    {
        "name": "get_seo_metrics",
        "description": (
            "Fetch Google Search Console SEO metrics for a date range. "
            "Returns total clicks, impressions, CTR, average position, "
            "top search queries with their individual metrics, and daily timeseries. "
            "Use this for any question about keyword rankings, organic search visibility, "
            "top queries, or search performance. Note: GSC has a ~3 day data lag."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "Start date in YYYY-MM-DD format",
                },
                "end_date": {
                    "type": "string",
                    "description": "End date in YYYY-MM-DD format",
                },
            },
            "required": ["start_date", "end_date"],
        },
    },
    {
        "name": "get_email_metrics",
        "description": (
            "Fetch Emma email marketing metrics for a date range. "
            "Returns total sends, open rate, click rate, and unsubscribe rate "
            "aggregated across all campaigns in the period, plus prior-period deltas. "
            "Use this for any question about email performance, campaign effectiveness, "
            "or audience engagement via email."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "Start date in YYYY-MM-DD format",
                },
                "end_date": {
                    "type": "string",
                    "description": "End date in YYYY-MM-DD format",
                },
            },
            "required": ["start_date", "end_date"],
        },
    },
    {
        "name": "get_social_metrics",
        "description": (
            "Fetch Sprout Social metrics for a date range. "
            "Returns impressions, engagements, reach, follower growth, top posts, "
            "and per-platform breakdowns across CBS Sprout profiles, plus prior-period deltas. "
            "Note: Sprout data excludes the most recent 2 days due to Facebook sync lag."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "Start date in YYYY-MM-DD format",
                },
                "end_date": {
                    "type": "string",
                    "description": "End date in YYYY-MM-DD format",
                },
            },
            "required": ["start_date", "end_date"],
        },
    },
    {
        "name": "generate_report",
        "description": (
            "Assemble a structured report artifact from fetched metrics. "
            "Call AFTER fetching the relevant channel metrics with the other tools. "
            "The artifact is persisted and can be exported to PDF, DOCX, PPTX, or CSV. "
            "Returns the report ID and a summary of what was included."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Report title, e.g. 'Q1 2025 Marketing Performance'",
                },
                "date_range_start": {
                    "type": "string",
                    "description": "Start date in YYYY-MM-DD format",
                },
                "date_range_end": {
                    "type": "string",
                    "description": "End date in YYYY-MM-DD format",
                },
                "channels": {
                    "type": "array",
                    "items": {"type": "string", "enum": ["web", "search", "email", "social"]},
                    "description": "Which channels to include in the report",
                },
                "executive_summary": {
                    "type": "string",
                    "description": "2–4 sentence executive summary of the period's performance",
                },
            },
            "required": ["title", "date_range_start", "date_range_end", "channels"],
        },
    },
]

# Default chat system prompt — orchestrator (see app.core.agents for specialists).
from app.core.agents import AGENTS

COSIGHT_SYSTEM_PROMPT = AGENTS["chat"].chat_system
