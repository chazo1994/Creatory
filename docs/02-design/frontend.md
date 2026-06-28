# Frontend Architecture (Creator Studio) — Design Layer

> **Layer:** Design. Module boundaries and runtime flow for the Studio. Current
> build status lives in
> [`../03-implementation/v0-snapshot.md`](../03-implementation/v0-snapshot.md).
> Backend orchestration boundaries are in [orchestration.md](orchestration.md).

Frontend source lives in `creatory_studio/` and follows Next.js App Router.

## Role Boundaries

- Frontend MUST focus on UX and client-side state orchestration.
- Backend MUST own state transitions and business invariants.
- Frontend MUST NOT duplicate backend orchestration logic, and MUST NOT decide
  business injection semantics (it calls the Bridge API — see
  [orchestration.md](orchestration.md) §4).

## Core Modules

- `DualChatPanel`: main stream + quick stream with `Add to Main Project` context injection.
- `WorkflowPanel`: visual workflow renderer/editor powered by React Flow.
- `AssetsPanel`: media storage listing and quick add.
- `PromptLabPanel`: create custom agent personas from UI.
- `SettingsCenter`: provider catalog, connection test, and routing preview.

## Data Layer

- `@tanstack/react-query` for API query/mutation orchestration.
- `zustand` store (`creatory_studio/src/store/studio-store.ts`) for global session/workspace/thread state.
- API client (`creatory_studio/src/lib/api.ts`) maps directly to backend endpoints.

## UI Direction

- Bento grid layout with glassmorphism-style panels.
- Color theme uses warm paper tones + accent orange + signal teal.
- Responsive design supports desktop and mobile by collapsing grid sections.

## Runtime Flow

1. User logs in/registers.
2. Workspace is selected/created.
3. Conversation is selected/created.
4. Threads are loaded (`main`, `quick`).
5. Dual chat sends prompt to orchestration endpoint.
6. Assistant response from quick stream can be injected into main stream context.
7. Workflow panel can run templates and show step states.

## Environment

- `NEXT_PUBLIC_API_URL` controls backend URL (default: `http://localhost:8000/api/v1`).
