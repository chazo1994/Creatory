from fastapi import APIRouter

from creatory_core.api.routes.agents import router as agents_router
from creatory_core.api.routes.assets import router as assets_router
from creatory_core.api.routes.auth import router as auth_router
from creatory_core.api.routes.conversations import router as conversations_router
from creatory_core.api.routes.health import router as health_router
from creatory_core.api.routes.knowledge import router as knowledge_router
from creatory_core.api.routes.mcp import router as mcp_router
from creatory_core.api.routes.orchestration import router as orchestration_router
from creatory_core.api.routes.providers import router as providers_router
from creatory_core.api.routes.workflows import router as workflows_router
from creatory_core.api.routes.workspaces import router as workspaces_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(workspaces_router)
api_router.include_router(conversations_router)
api_router.include_router(agents_router)
api_router.include_router(workflows_router)
api_router.include_router(mcp_router)
api_router.include_router(providers_router)
api_router.include_router(assets_router)
api_router.include_router(knowledge_router)
api_router.include_router(orchestration_router)
