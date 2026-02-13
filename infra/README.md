# Infrastructure

Deployment assets for Creatory.

- `docker-compose.yml`: primary full-stack composition.
- `docker-compose.dev.yml`: development overrides (hot reload and bind mounts).

Use from project root:

```bash
docker compose -f infra/docker-compose.yml up --build
docker compose -f infra/docker-compose.yml -f infra/docker-compose.dev.yml up --build
```
