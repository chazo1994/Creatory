# Contributing to Creatory

Creatory is a creator-first, agent-centric framework for building content pipelines.
This guide defines how to contribute safely and consistently.

## 1. Project Principles

- Creator-first UX: each feature should improve creator quality, speed, or control.
- Agent orchestration first: tools are coordinated by agents, not isolated utilities.
- Human-in-the-loop by default: creators can review and override key steps.
- Reusable workflows: successful pipelines should be templated and shareable.
- Production quality: tests, linting, reproducible setup, and observability are required.

## 2. Contribution Areas

1. MCP Tools: add MCP servers/tools for generation, editing, scraping, search, analytics.
2. Agent Personas: add specialized agents for specific creator workflows.
3. Workflow Templates: add reusable chat-based and node-based creator pipelines.
4. Frontend Studio: improve dual-chat UX, workflow editor nodes, and media/prompt modules.

## 3. Branch and Commit Rules

- Branch naming: `feat/<name>`, `fix/<name>`, `docs/<name>`, `refactor/<name>`.
- Commit format (Conventional Commits): `feat:`, `fix:`, `docs:`, `refactor:`, `test:`.

## 4. Pull Request Requirements

Each PR should include:

- Problem statement and proposed solution.
- Scope boundaries (what is intentionally excluded).
- Test evidence (unit/integration/e2e as relevant).
- Backward compatibility notes.
- Security/privacy impact for external integrations.

Keep PRs focused. Prefer small, single-purpose PRs.

## 5. MCP Tool Contribution Guide

### 5.1 Tool Contract

Each MCP tool must define:

- `tool_name`, `version`, and owner.
- Input schema (strict JSON Schema).
- Output schema (stable shape for downstream agents).
- Error contract (error code, message, retry guidance).
- Runtime constraints (timeout, rate-limit behavior, idempotency notes).

### 5.2 Suggested Layout

```text
packages/
  mcp/
    <tool-name>/
      README.md
      server.py
      schemas/
        input.schema.json
        output.schema.json
      tests/
        test_server.py
      examples/
        basic_request.json
```

### 5.3 MCP Checklist

- Validate input/output against schemas.
- Return machine-parseable errors.
- Add at least one success test and one failure test.
- Document auth requirements and env vars.
- Include a minimal request example.

## 6. Workflow Template Guide

A workflow template PR should include:

- Use case (example: short-form video from an article URL).
- Node list and role of each node.
- Human review checkpoints.
- Required tools and expected latency/cost profile.
- Failure handling and fallback strategy.

## 7. Agent Persona Guide

An agent persona PR should include:

- Persona goal and boundaries.
- System-prompt strategy and hard constraints.
- Required tools and preferred call order.
- Failure modes and safe fallback behavior.
- Evaluation samples (good vs bad outputs).

## 8. Quality Standards

- Test non-trivial logic.
- Keep modules cohesive and explicit.
- Prefer typed/validated schemas over implicit maps.
- Add logs for orchestration-critical operations.
- Avoid hidden side effects in tool execution paths.
- Ensure frontend changes pass `npm run lint` and `npm run build` in `frontend/`.

## 9. Security and Privacy

- Never commit secrets, tokens, or private credentials.
- Mask sensitive user data in logs/traces.
- Document retention policy when storing user data.
- State what external data is sent to third-party services.

## 10. RFC Requirements

Open an RFC issue before major changes:

- Database model changes.
- Orchestration protocol changes.
- Workflow runtime model changes.
- Breaking tool contract changes.

## 11. Database Change Rules

- Any schema change must include an Alembic revision in `alembic/versions/`.
- Keep SQL artifacts in `sql/migrations/` aligned with the revision.
- PRs touching schema must include an upgrade path and downgrade notes.

## 12. New Contributor Path

Recommended first contributions:

1. Improve docs in `docs/`.
2. Add a small workflow template.
3. Add tests for an existing tool or agent.

## 13. Definition of Done

A change is done when:

- Code and docs are aligned.
- Tests pass locally and in CI.
- Review feedback is resolved.
- Another contributor can use the change without verbal handoff.
