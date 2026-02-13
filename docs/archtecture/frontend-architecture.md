# Frontend Architecture (Creatory Studio V0)

Frontend source is located in `creatory_studio/` and follows Next.js App Router with `src/` layout.

## 1. Structure

```text
creatory_studio/
└── src/
    ├── app/
    │   ├── chat/
    │   ├── library/
    │   └── settings/
    ├── components/
    ├── hooks/
    ├── lib/
    └── store/
```

## 2. Core UI Modules

- `StudioApp`: authentication/workspace/conversation shell and module composition.
- `DualChatPanel`: main stream + quick stream + one-click context injection.
- `WorkflowPanel`: React Flow-based workflow visualization and run status.
- `AssetsPanel`: media asset listing and quick add.
- `PromptLabPanel`: quick agent persona creation.
- `SettingsCenter`: PAL provider catalog, connection test, routing preview.

## 3. State & Data Layer

- Server state: TanStack Query
- Client session state: Zustand (`src/store/studio-store.ts`)
- API client: `src/lib/api.ts`
- Domain types: `src/lib/types.ts`

## 4. Reusable Hooks

- `src/hooks/use-context-injection.ts`: encapsulates side-thread -> main-thread injection mutation.
- `src/hooks/use-run-stream.ts`: SSE run stream consumption for orchestration progress.

## 5. Routing

- `/chat`: full creator studio runtime
- `/library`: project/library module shell
- `/settings`: provider settings center (PAL)

## 6. UX Direction (Current)

- Bento-like panel composition
- Warm paper palette with teal/orange signals
- Desktop-first multi-panel layout with mobile collapse behavior

## 7. Runtime Contract with Backend

- Default backend base URL: `NEXT_PUBLIC_API_URL` (default `http://localhost:8000/api/v1`)
- All studio modules use `/api/v1/*` typed endpoints.
