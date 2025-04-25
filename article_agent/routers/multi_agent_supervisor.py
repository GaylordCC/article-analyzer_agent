from fastapi import APIRouter

from ..services.multi_agent_supervisor_service import MultiAgentSupervisor

router = APIRouter(
    tags=["Multi Agent Supervisor"]
)

@router.post("/multi-agent-supervisor")
async def multi_agent_supervisor():
    multi_agent_supervisor = MultiAgentSupervisor().create_supervisor()

    return {"result": multi_agent_supervisor}