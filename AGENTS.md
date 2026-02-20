# 🤖 AGENTS & ORCHESTRATION FRAMEWORK (CREATOR-FIRST)

Tài liệu này đồng bộ với bộ tài liệu mới nhất trong `docs/` gồm: `brainstorm.md`, `conceptual_blueprint_v0.md`, `archtecture/framework_architecture_v0.md`, `archtecture/frontend-architecture.md`, `requirements/business_requirements.md`, `roadmap/product_roadmap.md`.
Mục tiêu: Creator nghĩ, Agent điều phối, Workflow vận hành ổn định, cộng đồng mở rộng dễ dàng.

---

## 1. Product Vision (Creator-First)

- Nền tảng open source cho content creator, thiết kế để cộng đồng cùng contribute.
- Agent là trung tâm điều phối: planner, router, workflow coordinator, human-in-the-loop.
- Creator làm việc bằng chat và workflow node-based theo hướng agentic (không code-centric).
- Hỗ trợ mở rộng qua MCP tools, workflow templates, specialized agents.
- Triết lý: AI làm phần nặng, con người giữ chủ quyền sáng tạo (creative sovereignty).

---

## 2. Core Architecture (Stateful Orchestration)

Kiến trúc được tách rõ theo trách nhiệm để tránh chồng chéo.

### 2.1 Director Layer (Planning + State)

- Main Director Agent là điểm chạm chính cho creator.
- Chức năng:
  - Intention decoding từ prompt tự nhiên.
  - Lập kế hoạch task-level cho pipeline content.
  - Theo dõi trạng thái run/task trong conversation.
- Phối hợp PAL để chọn route model local/cloud theo task.
- Không chịu trách nhiệm chạy workflow graph node-by-node.

### 2.2 Workflow Runtime Layer (Execution)

- Workflow Runner thực thi template workflow theo nodes/edges.
- Hỗ trợ human gate node (`WAITING_HUMAN`) để bắt buộc review trước khi đi tiếp.
- Tách biệt khỏi Director để đảm bảo chat orchestration và graph execution độc lập, dễ test.

### 2.3 Dual-Stream Conversation + Bridge

- Conversation mặc định có 2 stream:
  - Main Stream: luồng chính cho chiến lược dài.
  - Quick Stream / Contextual Sub-Thread: luồng phụ cho thử nghiệm nhanh, quick Q&A; có thể là 1 side lane hoặc nhiều sub-thread theo ngữ cảnh.
- Bridge Injector là backend service duy nhất để inject context block từ quick stream vào main stream.
- Frontend chỉ gọi API inject, không re-implement business logic injection.
- Quy ước UX từ docs:
  - V0: split-screen main + quick.
  - Phase mở rộng: highlight-triggered contextual popup/sub-thread.

### 2.4 Guardrails (Safety & Governance)

- Circuit breaker giới hạn bước chạy để ngăn infinite loops.
- Hạn mức token/cost là guardrail bắt buộc khi mở rộng production scale.
- Human-in-the-loop là checkpoint an toàn và chất lượng, không chỉ là UX option.

---

## 3. Agentic Workflow Model

### 3.1 Chat-Based Workflow

- Creator gửi prompt ở stream chính.
- Director trả plan + routing và tạo các task orchestration.
- Chat-based workflow là mode vận hành của Director, không phải agent riêng.

### 3.2 Node-Based Workflow

- Node đại diện cho agent/tool/human gate.
- Edge đại diện cho luồng xử lý dữ liệu và điều kiện.
- Trạng thái hiện tại (V0):
  - Backend đã có workflow runtime đầy đủ để run template.
  - Frontend hiện là Visual Viewer/Runner (view + run + inspect step).
  - Node-based drag-and-drop authoring đầy đủ thuộc phase sau.

---

## 4. Knowledge Layer (Hybrid RAG)

- Một lớp duy nhất cho knowledge/retrieval, không tách thành nhiều module trùng chức năng.
- V0 hiện tại:
  - Lexical chunk ranking.
  - Concept graph bonus scoring.
  - Citation-based answer preview.
- Hỗ trợ dữ liệu nguồn đa dạng qua Knowledge Source/Chunk API.
- Hướng mở rộng theo docs: đa định dạng input (doc/link/image/audio/transcript) và citation traceability.

---

## 5. Tools & MCP Extension Layer

- MCP là chuẩn mở rộng tool runtime.
- Phân tách rõ:
  - Runtime/API: quản lý MCP server, tool, invocation.
  - Registry: manifest chuẩn cho tool ecosystem.
  - Contributor Track: hướng dẫn cách thêm MCP tools trong `CONTRIBUTING.md`.
- Trạng thái V0: invocation hiện ở mock runtime để validate orchestration contract trước khi gắn engine thật.
- Mục tiêu kiến trúc: thêm tools mới qua MCP mà không sửa core orchestrator.

---

## 6. Module Map (Repo-First)

- `creatory_core/`: backend engine (api, providers, rag, services, db).
- `creatory_studio/`: creator studio frontend (chat, library, settings, hooks).
- `mcp/`: server conventions + registry + sdk.
- `workflows/`: workflow templates + schemas.
- `infra/`: deployment assets.
- Root `docker-compose.yml`: compatibility; hạ tầng compose chuẩn đặt ở `infra/` theo tài liệu kiến trúc.

---

## 7. Frontend Architecture (Creator Studio)

### 7.1 Recommended Stack

- Next.js App Router.
- TanStack Query + Zustand.
- TailwindCSS + component system.
- React Flow cho workflow visualization.
- SSE/WebSocket cho stream run/task events.

### 7.2 Core Modules

| Module | Vai trò | Trạng thái |
| --- | --- | --- |
| Dual-Chat Interface | Main + Quick stream và gửi prompt | Implemented |
| Context Injection UX | "Add to Main Project" từ quick stream | Implemented (API-driven) |
| Workflow Panel | Hiển thị graph + run template + step status | Implemented (Viewer/Runner) |
| Prompt Lab / Assets / Settings | Không gian tinh chỉnh và quản trị studio | Implemented V0 |

### 7.3 Boundary Rule

- Frontend chịu trách nhiệm UX/state.
- Backend chịu trách nhiệm orchestration/state transition/injection normalization.
- Không duplicate logic nghiệp vụ giữa UI và service layer.

---

## 8. Runtime Stack & Deployment Topology

### 8.1 Runtime Stack

- Backend: FastAPI + orchestration services.
- Database: PostgreSQL + pgvector.
- Cache/queue: Redis.
- Frontend: Next.js studio.
- Auth/User management: tích hợp trong core API.

### 8.2 Deployment Topology

- Local/prod baseline qua Docker Compose.
- Services chuẩn:
  - `db`
  - `redis`
  - `migrate`
  - `api`
  - `agent-orchestrator`
  - `frontend`
- Canonical deployment assets đặt tại `infra/`.
- Root compose dùng cho compatibility tại repo root.

---

## 9. Current Implementation Status (Initialization Refactor)

- [x] Monorepo aligned: `creatory_core/`, `creatory_studio/`, `mcp/`, `workflows/`, `infra/`.
- [x] PAL endpoints V0: provider catalog, connection test, routing preview.
- [x] Hybrid RAG query endpoint với citation-style response scaffold.
- [x] Bridge injector runtime cho side-thread -> main-thread context block.
- [x] Starter workflow templates đặt tại `workflows/templates/`.

---

## 10. Contribution Model

Ưu tiên 3 hướng đóng góp:

1. MCP Tools: thêm server/tool contract theo registry + runtime API.
2. Workflow Templates: thêm template cho short-form, podcast, newsletter, campaign.
3. Specialized Agents: persona chuyên sâu theo domain (TikTok analyst, color grading advisor, SEO copy, v.v.).

Nguyên tắc:

- Mọi thay đổi lớn về orchestrator/workflow schema cần RFC.
- Đảm bảo code/docs/schema đồng bộ.
- Tôn trọng human-in-the-loop cho tác vụ sáng tạo quan trọng.

---

## 11. Product Roadmap (High-Level)

- [ ] Sprint 1: Core orchestration + dual-chat baseline.
- [ ] Sprint 2: Hybrid RAG integration + basic MCP toolchain.
- [ ] Sprint 3: Workflow visualization + robust run control.
- [ ] Sprint 4: Video/audio pipeline + community templates.
- [ ] Sprint 5: Full production hardening + contributor ecosystem scale.

---

> Motto: Creator nghĩ - Agent thực thi - Framework lan tỏa.
