# Founder Brainstorm (Original)

Nguồn: ý tưởng ban đầu của bạn trong phiên làm việc này.
Mục tiêu: lưu bản gốc để không bị mất/loãng ý khi refactor `AGENTS.md`.

## Ý Tưởng (Brainstorming)
- Tôi muốn xây dựng một opensource program trên github cho nhiều người cùng contribute.
- Sản phẩm hướng đến content creator theo thiên hướng mọi thứ phục vụ việc tạo content. (Creator First).
- Sản phẩm sử dụng AI Agent làm khung xương sống và cung cấp đầy đủ các công cụ để tạo thành content.
- Con người, creator sẽ giao tiếp với agent để lên ý tưởng, tạo khung, kịch bản,... lựa chọn sử dụng các công cụ cần thiết để tạo content. Làm sao để agent làm trung tâm điều phối, con người lên ý tưởng, tinh chỉnh thiết kế,...
- Con người có thể giao tiếp với agent bằng cách chat. Trong chat, cho phép con người quick question / comments + AI quick answer song song với main conversation, có thể inject info từ đoạn short conversation đó vào main conversation.
- Agents cung cấp cho con người rất nhiều công cụ tạo content, như video generation / edition, image generation / edition, audio generation / edition, text generation / edition, web search, web scraping,...
  - Agents: Hỗ trợ các hệ thống RAG, Hybrid RAG.
  - Agents: Hỗ trợ MCP với các tools.
- Sản phẩm sẽ có main agents, đây là agent giúp con người (Creator) brainstorming, tinh chỉnh, hiện thực hóa ý tưởng thành những công cụ và có thể save thành những pipeline, agent workflows.
  - Ngoài việc tinh chỉnh workflow trên main agents, người dùng còn có khu vực riêng chỉnh workflows dạng nodes. Nhưng là agentic workflow chứ không phải workflow về code.

Framework:
- Support production ready: Build pipeline, git pre commits, docker setup, docker compose.
- Quản lý user với database.
- Hỗ trợ nhiều loại input dữ liệu từ người dùng khác nhau.
- Và hướng tới là chuẩn framework opensource để nhiều người có thể contribute.

## AGENTS & ORCHESTRATION FRAMEWORK (CREATOR-FIRST)

Tài liệu quy định kiến trúc, cơ chế điều phối và tiêu chuẩn đóng góp cho hệ thống Multi-Agent trong dự án.
Mục tiêu là xây dựng một "Hệ điều hành trí tuệ" cho Content Creator.

### 1. Kiến trúc Tổng thể (Core Architecture)

Hệ thống được xây dựng trên mô hình Stateful Orchestration, kết hợp giữa tính linh hoạt của Chat và sự chặt chẽ của Workflow.

#### 1.1 Main Director Agent (The Brain)
- Vai trò: là điểm chạm duy nhất của Creator, giải mã ý tưởng (Intention Decoding).
- Nhiệm vụ:
  - Planning: chia nhỏ ý tưởng lớn thành task nhỏ cho sub-agents.
  - State Management: theo dõi tiến độ của toàn bộ pipeline content.
  - Persistence: đóng gói các luồng xử lý thành Workflow Templates để tái sử dụng.

#### 1.2 Dual-Stream Conversation (Innovation)
- Main Stream (Primary Thread): nơi định hình kịch bản, cấu trúc video, campaign dài hơi.
- Quick-Access Stream (Side-Bar Thread): câu hỏi nhanh, check thông tin, tạo thử mẫu ảnh/text.
- Bridge Injector: đẩy kết quả từ side-chat vào main stream dưới dạng Context Block.
- Ví dụ: tạo voice-over hay ở side-chat, 1 click inject vào đúng vị trí trong kịch bản chính.

### 2. Agentic Workflow & Nodes System

#### 2.1 Chat-based Workflow (Natural Language)
Creator yêu cầu: "Hãy tạo cho tôi một video TikTok từ bài báo này".
Main Agent tự động kích hoạt chuỗi Agent ngầm (RAG -> Script -> Image Gen -> Video Gen).

#### 2.2 Node-based Editor (Visual Programming)
- Không phải code workflow, mà là Agentic Workflow.
- Nodes: Agent Persona hoặc Tool (MCP).
- Edge: luồng suy nghĩ và dữ liệu.
- Human-in-the-loop Node: điểm dừng bắt buộc để creator review/chỉnh sửa trước khi qua node tiếp theo.

### 3. Hệ thống Tools & MCP
- Media Suite: Video/Image/Audio/Text Generation & Edition.
- Web Suite: Web Scraping (Firecrawl/Jina Reader), Web Search (Tavily/Perplexity).
- Production Suite: Git, Docker API để tự động deploy/push content.

### 4. Memory & Knowledge (Hybrid RAG)
- Vector Database: lưu tài liệu, web link, video cũ.
- Graph Database: lưu quan hệ concept, nhân vật, phong cách định kỳ.
- Input Support: Text, Image, Audio, file thiết kế thô.

### 5. Production-Ready Framework
- Core Logic: Python (FastAPI + LangGraph).
- Database: PostgreSQL + pgvector.
- DevOps: docker-compose, git pre-commit hooks.
- Quản lý User/Auth tích hợp.

### 6. Hướng dẫn Contributor (Contribution Guide)
- New MCP Tools.
- Workflow Templates.
- Specialized Agents.

### 7. Frontend Architecture: The Creator Studio
- Tech stack: Next.js App Router, TanStack Query + Zustand, ShadcnUI + TailwindCSS, React Flow, SSE/WebSocket.
- Core Modules:
  - Dual-Chat Interface.
  - Visual Workflow Editor.
  - Media Asset Manager.
  - Prompt Engineering Lab.
- Injection UI:
  - Side-bar có button "Add to Main Project".
  - Frontend gán Reference ID vào context main chat qua API.

### 8. Production-Ready Deployment (Full-stack)
- Frontend
- Backend API
- Agent orchestrator
- DB (pgvector)
- Redis

### 9. Hướng dẫn đóng góp Frontend
- Custom Nodes.
- Theme Engine.
- Performance Optimization.

### Roadmap
- Sprint 1: Core Architecture + Dual-chat.
- Sprint 2: RAG + basic MCP tools.
- Sprint 3: Visual Node Editor.
- Sprint 4: Video/Audio pipeline + templates.
- Sprint 5: Full production ready + frontend.

Motto: Creator nghĩ - Agent thực thi - Framework lan tỏa.
