# 🗺️ CREATORY: VERTICAL SLICE ROADMAP (12-WEEK SPRINT)

**Chiến lược:** Product-First & Local-First.
**Tiêu chí:** Mỗi Phase đều phải release được một tính năng chạy trọn vẹn từ Backend $\rightarrow$ Frontend $\rightarrow$ AI Output.

---

## 🚩 PHASE 1: THE "HELLO WORLD" CREATOR (Tuần 1 - 4)
**Mục tiêu:** Xây dựng một "Local Creative Engine" tối giản. Người dùng có thể tạo một **Project**, upload tài liệu, và yêu cầu AI thực hiện chuỗi tác vụ đa phương tiện (Research + Write + Draw + Speak).

### 🎯 Deliverable (Kết quả bàn giao)
Một ứng dụng chạy local (Docker) cho phép:
1.  Tạo Project "Youtube Script A".
2.  Upload PDF/Text (RAG cơ bản).
3.  Chat: "Hãy nghiên cứu chủ đề này, viết kịch bản, tạo ảnh thumbnail và đọc lời thoại mở đầu."
4.  Kết quả: Text kịch bản + 1 File Ảnh + 1 File Audio.

### ✅ Detailed Checklist & Tasks

#### 1. Core Architecture (Backend & Project Structure)
- [ ] **Init Repo:** Cấu trúc Monorepo (FastAPI + Next.js).
- [ ] **Project-Centric DB:** Thiết kế Schema PostgreSQL/SQLite tập trung vào `ProjectID`.
    - *Lưu ý:* Mọi file upload, vector index, và lịch sử chat đều phải gắn với `project_id`, không phải global.
- [ ] **Local LLM Integration:**
    - [ ] Hỗ trợ chuyển đổi: OpenAI (Cloud) $\leftrightarrow$ Ollama (Local) qua biến môi trường `.env`.
- [ ] **Safety Layer (Circuit Breaker v1):**
    - [ ] Implement `max_steps=10` hard-limit trong vòng lặp LangGraph để chống treo máy.

#### 2. AI Tools (Simple Binding - No MCP Server yet)
*Tích hợp trực tiếp function vào Agent để chạy được ngay.*
- [ ] **Simple RAG (NotebookLM style):**
    - [ ] Sử dụng `ChromaDB` (local). Upload file $\rightarrow$ Chunking $\rightarrow$ Retrieval.
- [ ] **Web Search:** Tích hợp Tavily API (Free tier).
- [ ] **Image Gen:** Tích hợp Flux (qua API HuggingFace hoặc Local mock) hoặc DALL-E 3.
- [ ] **Text-to-Speech (TTS):** Tích hợp `Edge-TTS` (Python library, miễn phí, chạy local ngon) hoặc gTTS đơn giản.

#### 3. Frontend (MVP)
- [ ] **Project Dashboard:** Danh sách các dự án đã tạo.
- [ ] **Chat Interface:** Giao diện chat đơn giản (như ChatGPT).
- [ ] **Media Rendering:**
    - [ ] Hiển thị ảnh Markdown `![image](url)` ngay trong khung chat.
    - [ ] Hiển thị Audio Player `<audio>` ngay dưới tin nhắn AI.

---

## 🚩 PHASE 2: DUAL-STREAM & VISUAL VIEWER (Tuần 5 - 8)
**Mục tiêu:** Nâng cấp trải nghiệm UX độc nhất (USP). Tách luồng "Sáng tạo" và "Tra cứu". Hiển thị quy trình tư duy của Agent dưới dạng hình ảnh.

### 🎯 Deliverable (Kết quả bàn giao)
1.  Giao diện 2 cột: Main Editor & Context Chat.
2.  Tính năng "Bridge Injection" (Bắn tin từ phụ sang chính).
3.  Tab "Workflow View": Nhìn thấy sơ đồ Agent đang chạy (Read-only).

### ✅ Detailed Checklist & Tasks

#### 1. Frontend (Dual-Stream UX)
- [ ] **Split Pane Layout:** Cột trái (Main Editor/Chat) - Cột phải (Context/Sub-chat).
- [ ] **Context Action:**
    - [ ] Bôi đen text cột trái $\rightarrow$ Hiện nút "Ask AI" $\rightarrow$ Mở cột phải.
- [ ] **Bridge Mechanism:**
    - [ ] Nút "Inject to Main": Lấy nội dung tóm tắt từ cột phải, chèn vào context của cột trái.

#### 2. Workflow Logic (Code-based)
- [ ] **YAML Workflows:** Định nghĩa các quy trình chuẩn bằng file YAML (VD: `blog_post_workflow.yaml`).
    - *Lợi ích:* Contributor có thể viết workflow mà không cần sửa code Python.
- [ ] **Workflow Visualization (Read-only):**
    - [ ] Dùng `ReactFlow` hoặc `Mermaid` để render file YAML thành sơ đồ khối trên UI.
    - [ ] Highlight node đang chạy (Real-time status qua WebSocket).

#### 3. Advanced Safety (Circuit Breaker v2)
- [ ] **Token Counter:** Đếm token input/output.
- [ ] **Cost Guard:** Tự động ngắt nếu chi phí ước tính vượt quá $X (nếu dùng API trả phí).
- [ ] **Loop Detection:** Phát hiện nếu Agent lặp lại cùng một câu trả lời 3 lần liên tiếp.

---

## 🚩 PHASE 3: EXTENSIBILITY & PRODUCTION READY (Tuần 9 - 12)
**Mục tiêu:** Chuẩn hóa hệ thống để cộng đồng đóng góp (MCP) và tối ưu hóa RAG/Memory.

### 🎯 Deliverable (Kết quả bàn giao)
1.  Hệ thống Plugin qua chuẩn MCP.
2.  Hybrid RAG (Graph + Vector) để nhớ style người dùng.
3.  Docker Compose "1-Click" cho người dùng phổ thông.

### ✅ Detailed Checklist & Tasks

#### 1. MCP Implementation (Chuẩn hóa Tools)
- [ ] **MCP Client:** Refactor các tools ở Phase 1 (Search, Image, TTS) thành các **MCP Servers** độc lập.
- [ ] **Tool Registry:** File `registry.json` để quản lý danh sách tools.
- [ ] **Contributor Guide:** Hướng dẫn viết tool mới (VD: Tool lấy dữ liệu chứng khoán, Tool gửi Email).

#### 2. Advanced Memory (RAG Upgrade)
- [ ] **User Persona:** Lưu trữ "Style viết" của user vào Vector DB để Agent bắt chước giọng văn.
- [ ] **Graph Knowledge (Optional/Lite):** Thử nghiệm Neo4j hoặc NetworkX để lưu mối quan hệ giữa các nhân vật/khái niệm trong Project.

#### 3. DevOps & Polish
- [ ] **Docker Profiles:**
    - [ ] `docker-compose.yml` (Standard): Dùng OpenAI/Cloud API.
    - [ ] `docker-compose.local.yml`: Kèm sẵn service Ollama + Qdrant/Chroma self-hosted.
- [ ] **CI/CD:** Github Actions để test các Workflow YAML tự động.
- [ ] **Documentation:** Viết Wiki đầy đủ cho User và Developer.

---

### 💡 Gợi ý cho Contributor (Good First Issues)

Để thu hút cộng đồng ngay từ Phase 1, bạn có thể tạo các Issue sau trên GitHub:

1.  **"Add new TTS Provider":** Viết function Python wrapper cho ElevenLabs hoặc OpenAI TTS.
2.  **"Improve PDF Parser":** Tối ưu hóa cách cắt file PDF (Chunking strategy) cho RAG.
3.  **"Add Dark Mode":** UI task đơn giản cho Frontend dev.
4.  **"Create Prompt Template":** Viết file YAML prompt cho các tác vụ như "Viết bài SEO", "Tóm tắt Video".

Roadmap này đảm bảo bạn có **Tech (Phase 1)** $\rightarrow$ **UX (Phase 2)** $\rightarrow$ **Ecosystem (Phase 3)** mà không bị sa lầy vào việc code những tính năng chưa cần thiết.