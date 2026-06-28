# Workflows DNA

Shared workflow blueprints live here.

- `templates/`: reusable YAML templates that can be imported by the director.
- `schemas/`: JSON schema contracts for validating templates.

These files are intended to be version-controlled and community-contributed.

> The **canonical design** of the node/edge model (node types, edges,
> `condition_expr`, join policy, HITL) lives in
> [`../docs/02-design/workflow-model.md`](../docs/02-design/workflow-model.md).
> That design is the source of truth over this schema and any code; gaps are
> tracked in
> [`../docs/03-implementation/divergence-log.md`](../docs/03-implementation/divergence-log.md).
