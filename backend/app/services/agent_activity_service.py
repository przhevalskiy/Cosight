"""Latest discussion snippet per dashboard specialist agent."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from app.core.agents import resolve_chat_agent
from app.services.cosight_discussion_service import get_cosight_discussion_service

logger = logging.getLogger(__name__)

ROSTER_AGENT_IDS = ("overview", "web", "search", "email", "social", "reports")


def _snippet(text: str, max_len: int = 96) -> str:
    cleaned = " ".join(text.split())
    if len(cleaned) <= max_len:
        return cleaned
    return cleaned[: max_len - 1].rstrip() + "…"


def _message_preview(discussion_id: str) -> str:
    svc = get_cosight_discussion_service()
    messages = svc.get_context_messages(discussion_id, limit=8)
    for msg in reversed(messages):
        content = (msg.content or "").strip()
        if not content or content.startswith("__"):
            continue
        return _snippet(content)
    return ""


def get_agent_activity() -> List[Dict[str, Any]]:
    """
    For each roster agent, return the most recent discussion preview (if any).
    Uses stored agent_id when present; otherwise classifies from message text.
    """
    svc = get_cosight_discussion_service()
    try:
        discussions = svc.list_discussions()[:80]
    except Exception as exc:
        logger.warning("Agent activity: could not list discussions: %s", exc)
        discussions = []

    best: Dict[str, Dict[str, Any]] = {}

    for disc in discussions:
        agent_id: Optional[str] = getattr(disc, "agent_id", None)
        preview = _message_preview(disc.id)
        if not agent_id and preview:
            agent_id = resolve_chat_agent(preview).id
        if agent_id == "chat":
            agent_id = "overview"
        if agent_id not in ROSTER_AGENT_IDS:
            continue
        if not preview and disc.title and disc.title != "New Chat":
            preview = _snippet(disc.title)

        updated = disc.updated_at
        if isinstance(updated, str):
            try:
                updated = datetime.fromisoformat(updated.replace("Z", "+00:00"))
            except ValueError:
                updated = datetime.utcnow()

        prev = best.get(agent_id)
        if prev and prev["_updated"] >= updated:
            continue

        best[agent_id] = {
            "agent_id": agent_id,
            "discussion_id": disc.id,
            "snippet": preview or None,
            "updated_at": str(disc.updated_at),
            "_updated": updated,
        }

    result: List[Dict[str, Any]] = []
    for agent_id in ROSTER_AGENT_IDS:
        entry = best.get(agent_id)
        result.append({
            "agent_id": agent_id,
            "discussion_id": entry["discussion_id"] if entry else None,
            "snippet": entry["snippet"] if entry else None,
            "updated_at": entry["updated_at"] if entry else None,
        })
    return result
