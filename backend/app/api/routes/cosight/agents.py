"""Agent registry metadata for UI."""
from fastapi import APIRouter

from app.core.agents import list_agents_public
from app.services.agent_activity_service import get_agent_activity

router = APIRouter(prefix="/api/cosight/agents", tags=["cosight-agents"])


@router.get("")
async def list_agents():
    return list_agents_public()


@router.get("/activity")
async def agent_activity():
    return get_agent_activity()
