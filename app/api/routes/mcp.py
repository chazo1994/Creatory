import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.api.permissions import ensure_workspace_member
from app.db.models import MCPServer, MCPTool, RunStatus, ToolInvocation, User
from app.db.session import get_db_session
from app.schemas.mcp import (
    MCPServerCreateRequest,
    MCPServerRead,
    MCPToolCreateRequest,
    MCPToolRead,
    ToolInvocationRead,
)

router = APIRouter(prefix="/mcp", tags=["mcp"])


@router.post("/servers", response_model=MCPServerRead, status_code=status.HTTP_201_CREATED)
async def create_server(
    payload: MCPServerCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> MCPServerRead:
    await ensure_workspace_member(db, payload.workspace_id, current_user.id)

    server = MCPServer(
        workspace_id=payload.workspace_id,
        name=payload.name,
        transport=payload.transport,
        endpoint=payload.endpoint,
        auth_config_json=payload.auth_config_json,
        is_active=payload.is_active,
    )
    db.add(server)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="MCP server already exists in this workspace",
        ) from None

    await db.refresh(server)
    return MCPServerRead.model_validate(server)


@router.get("/servers", response_model=list[MCPServerRead])
async def list_servers(
    workspace_id: uuid.UUID,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[MCPServerRead]:
    await ensure_workspace_member(db, workspace_id, current_user.id)

    result = await db.scalars(
        select(MCPServer)
        .where(MCPServer.workspace_id == workspace_id)
        .order_by(MCPServer.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return [MCPServerRead.model_validate(item) for item in result.all()]


@router.post(
    "/servers/{mcp_server_id}/tools",
    response_model=MCPToolRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_tool(
    mcp_server_id: uuid.UUID,
    payload: MCPToolCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> MCPToolRead:
    server = await db.get(MCPServer, mcp_server_id)
    if server is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MCP server not found")

    await ensure_workspace_member(db, server.workspace_id, current_user.id)

    tool = MCPTool(
        mcp_server_id=server.id,
        tool_name=payload.tool_name,
        description=payload.description,
        input_schema=payload.input_schema,
        output_schema=payload.output_schema,
        capabilities_json=payload.capabilities_json,
    )
    db.add(tool)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tool already exists on this MCP server",
        ) from None

    await db.refresh(tool)
    return MCPToolRead.model_validate(tool)


@router.get("/servers/{mcp_server_id}/tools", response_model=list[MCPToolRead])
async def list_tools(
    mcp_server_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[MCPToolRead]:
    server = await db.get(MCPServer, mcp_server_id)
    if server is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MCP server not found")
    await ensure_workspace_member(db, server.workspace_id, current_user.id)

    tools = (
        await db.scalars(
            select(MCPTool)
            .where(MCPTool.mcp_server_id == mcp_server_id)
            .order_by(MCPTool.created_at.asc())
        )
    ).all()
    return [MCPToolRead.model_validate(item) for item in tools]


@router.post("/tools/{tool_id}/invoke", response_model=ToolInvocationRead)
async def invoke_tool(
    tool_id: uuid.UUID,
    payload: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> ToolInvocationRead:
    tool = await db.get(MCPTool, tool_id)
    if tool is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MCP tool not found")

    server = await db.get(MCPServer, tool.mcp_server_id)
    if server is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MCP server not found")

    await ensure_workspace_member(db, server.workspace_id, current_user.id)

    invocation = ToolInvocation(
        task_id=None,
        workflow_run_step_id=None,
        mcp_tool_id=tool.id,
        request_json=payload,
        response_json={
            "ok": True,
            "tool": tool.tool_name,
            "mock": True,
            "message": "Invocation executed through framework mock runtime.",
        },
        status=RunStatus.SUCCEEDED,
    )
    db.add(invocation)
    await db.commit()
    await db.refresh(invocation)

    return ToolInvocationRead.model_validate(invocation)
