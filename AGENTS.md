# Ý Tưởng (Brainstorming)
- Tôi muốn xây dựng một opensource program trên github cho nhiều người cùng contribute.
- Sản phẩm hướng đến content creator theo thiên hướng mọi thứ phục vụ việc tạo content. (Creator First).
- Sản phẩm sử dụng AI Agent làm khung sương sống và cung cấp đầy đủ các công cụ để tạo thành content.
- Con người, creator sẽ giao tiếp với agent để lên ý tưởng, tạo khung, kịch bản,... lựa chọn sử dụng các công cụ cần thiết để tạo content. Làm sao để agent làm trung tâm điều phối, con người lên ý tưởng, tinh chỉnh thiết kế,...
- Con người có thể giao tiếp với agent bằng cách chat. Trong chat, cho phép con người quick question / comments + ai quick answer song song với main conversation, có thể inject info từ đoạn short conversation đó vào main conversation.
- Agents cung cấp cho con người rất nhiều công cụ tạo content, như video generation / edition, image generation / edition, audio generation / edition, text generation / edition, web search, web scraping,…
	- Agents: Hỗ trợ các hệ thống RAG, Hybrid RAG.
	- Agents: Hỗ trợ mcp với các tools.
- Sản phẩm sẽ có main agents đây là agent giúp con người (Creator) brainstorming, tinh chỉnh, hiện thực hóa ý tưởng thành những công cụ và có thể save thành những pipeline, agent workflows.
	- Ngoài việc tinh chỉnh workflow trên main agents, người dùng còn có khu vực riêng chỉnh workflows dạng nodes. Nhưng là agentic workflow chứ không phải workflow về code. 
Framework:
Support production ready: Build pipeline, git pre commits, docker setup, docker compose.
Quản lý user với database.
Hỗ trợ nhiều loại input dữ liệu từ người dùng khác nhau.
- Và hướng tới là chuẩn framework opensource để nhiều người có thể contribute.

---

# 🤖 AGENTS & ORCHESTRATION FRAMEWORK (CREATOR-FIRST)

Tài liệu này quy định kiến trúc, cơ chế điều phối và tiêu chuẩn đóng góp cho hệ thống **Multi-Agent** trong dự án. Mục tiêu là xây dựng một "Hệ điều hành trí tuệ" cho Content Creator.

---

## 🧩 1. Kiến trúc Tổng thể (Core Architecture)

Hệ thống được xây dựng trên mô hình **Stateful Orchestration**, kết hợp giữa tính linh hoạt của Chat và sự chặt chẽ của Workflow.

### 1.1. Main Director Agent (The Brain)

* **Vai trò:** Là điểm chạm duy nhất của Creator. Chịu trách nhiệm giải mã ý tưởng (Intention Decoding).
* **Nhiệm vụ:**
* Lập kế hoạch (Planning): Chia nhỏ ý tưởng lớn thành các Task nhỏ cho Sub-agents.
* Quản lý trạng thái (State Management): Theo dõi tiến độ của toàn bộ pipeline content.
* Lưu trữ (Persistence): Có khả năng đóng gói các luồng xử lý thành các **Workflow Templates** để tái sử dụng.



### 1.2. Dual-Stream Conversation (Innovation)

Cơ chế tương tác độc quyền cho phép Creator làm việc đa nhiệm mà không mất context:

* **Main Stream (Primary Thread):** Nơi định hình kịch bản, cấu trúc video, hoặc chiến dịch marketing dài hơi.
* **Quick-Access Stream (Side-Bar Thread):**
* Dành cho các câu hỏi nhanh, kiểm tra thông tin hoặc tạo thử mẫu ảnh/text.
* **Bridge Injector:** Một cơ chế cho phép "đẩy" (inject) kết quả từ Side-chat vào Main Stream dưới dạng `Context Block`.
* *Ví dụ:* Bạn tạo một đoạn voice-over hay ở side-chat, chỉ cần 1 click để "Inject" nó vào đúng vị trí trong kịch bản chính ở Main Stream.



---

## 🛠 2. Agentic Workflow & Nodes System

Chúng ta phân biệt rõ hai khu vực làm việc:

### 2.1. Chat-based Workflow (Natural Language)

Creator yêu cầu: *"Hãy tạo cho tôi một video TikTok từ bài báo này"*. Main Agent sẽ tự động kích hoạt một chuỗi Agent ngầm (RAG Agent -> Script Agent -> Image Gen Agent -> Video Gen Agent).

### 2.2. Node-based Editor (Visual Programming)

Khu vực dành cho việc tinh chỉnh chuyên sâu. Đây **không phải là Code Workflow**, mà là **Agentic Workflow**:

* **Nodes:** Mỗi node đại diện cho một Agent Persona hoặc một Tool (MCP).
* **Edge:** Đại diện cho luồng suy nghĩ (Reasoning Flow) và dữ liệu.
* **Human-in-the-loop Node:** Điểm dừng bắt buộc để Creator review, chỉnh sửa kịch bản/hình ảnh trước khi chuyển sang node kế tiếp.

---

## 🧰 3. Hệ thống Tools & MCP (Model Context Protocol)

Để dự án có thể mở rộng vô hạn bởi cộng đồng, chúng ta sử dụng chuẩn **MCP**:

* **Media Suite:** Tích hợp các Engine hàng đầu (Video/Image/Audio/Text Generation & Edition).
* **Web Suite:** Các công cụ Web Scraping (Firecrawl/Jina Reader), Web Search (Tavily/Perplexity) để cập nhật trend thời gian thực.
* **Production Suite:** Tích hợp Git, Docker API để tự động hóa việc deploy/push content.

---

## 📚 4. Memory & Knowledge (Hybrid RAG)

Hệ thống sử dụng cơ chế **Hybrid RAG** để Agent không bao giờ "quên" phong cách của Creator:

* **Vector Database:** Lưu trữ dữ liệu từ tài liệu, link web, video cũ của Creator.
* **Graph Database:** Lưu trữ mối quan hệ giữa các concept, nhân vật, và phong cách định kỳ của Creator.
* **Input Support:** Hỗ trợ đa dạng từ Text, Image, Audio đến các file thô từ thiết kế.

---

## 🚢 5. Production-Ready Framework

Dự án được thiết kế để triển khai ngay lập tức (Ready for Contributors):

* **Core Logic:** Python (FastAPI + LangGraph).
* **Database:** PostgreSQL (User data) + pgvector (Long-term memory).
* **DevOps:** * `docker-compose.yml` tích hợp sẵn đầy đủ môi trường.
* Git pre-commit hooks để check chất lượng code/prompt.
* Quản lý User/Auth tích hợp sẵn.



---

## 🤝 6. Hướng dẫn Contributor (Contribution Guide)

Chúng tôi mong đợi sự đóng góp ở 3 mảng chính:

1. **New MCP Tools:** Viết các server MCP để kết nối thêm các công cụ AI mới (Sora, Flux, Kling, v.v.).
2. **Workflow Templates:** Thiết kế các mẫu node-based workflow tối ưu cho các loại content khác nhau (Short-form, Podcast, Newsletter).
3. **Specialized Agents:** Xây dựng các Agent Persona chuyên biệt (Ví dụ: Agent chuyên phân tích thuật toán TikTok, Agent chuyên chỉnh sửa màu sắc video).

---
Đúng là thiếu sót lớn nếu một sản phẩm **Creator-First** mà không có một giao diện (Frontend) cực đỉnh. Đối với Creator, trải nghiệm thị giác và thao tác kéo thả (UX/UI) quan trọng ngang ngửa với sức mạnh của AI.

Dưới đây là phần bổ sung chi tiết về **Frontend Architecture** để đưa vào tài liệu, đảm bảo tính "Production-ready" và hỗ trợ cộng đồng dễ dàng đóng góp.

---

## 🎨 7. Frontend Architecture: The Creator Studio

Giao diện được thiết kế theo phong cách **Bento Grid** hiện đại, tập trung vào việc giảm thiểu số click và tối đa hóa không gian sáng tạo.

### 7.1. Tech Stack Khuyến nghị

* **Framework:** Next.js 14/15 (App Router) - Tối ưu SEO cho các trang public của creator.
* **State Management:** TanStack Query (React Query) + Zustand (cho nhẹ và nhanh).
* **UI Component:** ShadcnUI + TailwindCSS.
* **Workflow Engine:** **React Flow** (Dành riêng cho khu vực chỉnh sửa Node-based Agentic Workflow).
* **Real-time:** WebSockets hoặc Server-Sent Events (SSE) để stream câu trả lời từ Agent và cập nhật tiến độ render media.

### 7.2. Các phân khu chức năng (Core Modules)

| Module | Chức năng chính | Key Features |
| --- | --- | --- |
| **Dual-Chat Interface** | Giao diện tương tác chính | Chia màn hình: Main Chat (Trái) & Side-bar Chat (Phải). Hỗ trợ Markdown, Code Highlight, và Media Preview trực tiếp. |
| **Visual Workflow Editor** | Khu vực tùy chỉnh "khung xương" | Giao diện kéo thả Nodes. Cho phép Creator nhìn thấy luồng tư duy của Agent. Có nút "Run Step-by-Step" để debug. |
| **Media Asset Manager** | Quản lý thành phẩm | Nơi lưu trữ ảnh, video, audio đã tạo. Có trình xem (Viewer) và trình chỉnh sửa nhanh (Quick Editor). |
| **Prompt Engineering Lab** | Tinh chỉnh "linh hồn" Agent | Khu vực dành cho contributor và user nâng cao để test các System Prompts và Tool parameters. |

### 7.3. Cơ chế "Injection" UI (Frontend Logic)

* Tại Side-bar Chat, mỗi block kết quả (ví dụ một đoạn script hoặc link ảnh) sẽ có một button **"Add to Main Project"**.
* Khi click, Frontend sẽ gán một `Reference ID` từ Side-chat vào Context của Main Chat thông qua API, giúp Agent chính nhận diện được dữ liệu đó mà không cần user phải copy-paste.

---

## 🏗️ 8. Production-Ready Deployment (Full-stack)

Để dự án thực sự là một Open Source Framework chuẩn chỉnh, cấu trúc Docker ví dụ mẫu:

```yaml
# docker-compose.yml (Phác thảo)
services:
  frontend:
    build: ./creatory_studio
    ports: ["3000:3000"]
    environment: [NEXT_PUBLIC_API_URL]
    
  backend-api:
    build: .
    depends_on: [db, redis]
    
  agent-orchestrator:
    build: .
    # Chạy LangGraph / LangServe
    
  db:
    image: ankane/pgvector # Postgres hỗ trợ Vector
    
  redis:
    image: redis:alpine # Quản lý hàng chờ render media và cache chat

```

---

## 🚢 9. Hướng dẫn đóng góp Frontend (Frontend Contributors)

Chúng tôi tìm kiếm các đóng góp về:

1. **Custom Nodes:** Thiết kế các UI components cho từng loại Agent Node (VD: Node tạo ảnh có thanh slider chỉnh Aspect Ratio).
2. **Theme Engine:** Hỗ trợ Dark/Light mode và các Theme tùy biến cho Creator.
3. **Performance Optimization:** Xử lý render các danh sách media lớn (Virtual Scroll) và tối ưu hóa việc stream dữ liệu từ AI.

---

## 📈 7. Roadmap Phát triển

* [ ] **Sprint 1:** Core Architecture & Dual-chat Interface.
* [ ] **Sprint 2:** RAG Integration & Basic MCP Tools (Text/Image).
* [ ] **Sprint 3:** Visual Node Editor (Agentic Workflow).
* [ ] **Sprint 4:** Video/Audio Generation Pipeline & Community Templates.
* [ ] **Sprint 5:** Full hệ thống, production ready + front end.

---

> **Motto:** Creator nghĩ - Agent thực thi - Framework lan tỏa.

---

### Gợi ý tiếp theo cho bạn:

1. Bạn có muốn tôi viết file **`CONTRIBUTING.md`** để hướng dẫn chi tiết cách một developer có thể viết một **MCP Tool** mới cho dự án này không?
2. Hay bạn muốn tôi phác thảo **Database Schema** để quản lý các "Agent State" và "User Workflow"?
