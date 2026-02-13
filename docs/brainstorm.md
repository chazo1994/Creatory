# 🧠 TÀI LIỆU Ý TƯỞNG HỆ THỐNG: CREATORY

**Tầm nhìn:** Xây dựng một "Hệ điều hành trí tuệ" (Intellectual OS) dành riêng cho Content Creator, lấy AI Agent làm xương sống để tối ưu hóa quy trình từ ý tưởng đến thành phẩm.

---

### 1. Triết lý Phát triển (Core Philosophy)

* **Creator-First:** Mọi công cụ và luồng xử lý đều xoay quanh việc giải phóng sức sáng tạo của con người, không thay thế con người.
* **Open Source:** Xây dựng trên nền tảng mã nguồn mở (GitHub) để cộng đồng cùng đóng góp Agent Personas, MCP Tools và Workflow Templates.
* **Agentic Orchestration:** AI không chỉ là chatbot mà là người điều phối (Orchestrator), kết nối các công cụ rời rạc thành một pipeline hoàn chỉnh.

### 2. Hệ thống Tương tác Đa luồng (Multi-thread Interaction)

Đây là điểm sáng tạo cốt lõi trong giao tiếp giữa Người và Máy:

* **Main Conversation (Luồng chính):**
* Nơi Creator giao tiếp trực tiếp với **Main Director Agent**.
* Tập trung vào việc lên chiến lược, phác thảo cấu trúc nội dung và điều phối tổng thể dự án.


* **Contextual Sub-Thread (Luồng phụ theo ngữ cảnh):**
* **Cơ chế kích hoạt:** Khi người dùng bôi đen một đoạn văn bản hoặc click vào một điểm cụ thể trong nội dung, một popup/panel sẽ hiện ra.
* **Tính biệt lập (Isolation):** Đây là các cuộc hội thoại ngắn (Quick Q&A) để làm rõ thuật ngữ, tra cứu thông tin nhanh hoặc thảo luận về một chi tiết nhỏ. Luồng này có context riêng, không làm nhiễu luồng tư duy chính của Director Agent.
* **Cơ chế Injection (Kết chuyển):** Người dùng có quyền lựa chọn "Inject" (tóm tắt hoặc kết quả cuối cùng) từ luồng phụ này vào Context của luồng chính để cập nhật kịch bản hoặc kế hoạch hành động.



### 3. Hệ điều hành Agent (Agentic Framework)

* **Main Director Agent:** Đóng vai trò "Quản trị dự án", có khả năng lập kế hoạch (Planning), chia nhỏ Task và phân quyền cho các Sub-agents.
* **Agentic Workflow (Visual Node Editor):**
* Cung cấp khu vực chỉnh sửa dạng Nodes (kéo thả) để tinh chỉnh quy trình.
* **Lưu ý:** Đây là Workflow về tư duy Agent (Agentic reasoning), không phải workflow lập trình thuần túy.
* Cho phép lưu các luồng xử lý thành các **Pipeline/Templates** để tái sử dụng hoặc chia sẻ.


* **Human-in-the-loop (HITL):** Tích hợp các điểm dừng bắt buộc để con người kiểm duyệt, tinh chỉnh trước khi Agent chuyển sang bước tiếp theo.

### 4. Hệ sinh thái Công cụ & Dữ liệu

* **Hỗ trợ MCP (Model Context Protocol):** Kết nối không giới hạn với các công cụ tạo nội dung (Video, Image, Audio, Text generation/edition), Web Search, Web Scraping thông qua các server MCP độc lập.
* **Memory & Knowledge (Hybrid RAG):**
* Sử dụng kết hợp **Vector RAG** (tra cứu tài liệu) và **Graph RAG** (quản lý mối quan hệ thực thể và phong cách riêng của Creator).
* Hỗ trợ đa dạng input: Text, Image, Audio, và các file thô từ thiết kế.



### 5. Tiêu chuẩn Production-Ready

* **Cấu trúc kỹ thuật:** Xây dựng trên nền tảng Python (FastAPI + LangGraph) và Next.js.
* **Hệ thống Hậu cần:** Quản lý User/Auth, quản lý phiên (Session/Thread), cơ sở dữ liệu (PostgreSQL + pgvector).
* **DevOps:** Hỗ trợ Docker, Docker Compose, Git pre-commit hooks để đảm bảo quy chuẩn đóng góp mã nguồn mở chuyên nghiệp.

---

> **Mục tiêu cuối cùng:** Biến Creatory thành chuẩn framework mã nguồn mở hàng đầu, nơi mọi Creator có thể tùy biến "linh hồn" AI của riêng mình để hiện thực hóa mọi ý tưởng.

---

### 🚀 Tiếp theo bạn có muốn tôi làm gì?

Bản đặc tả đã hoàn thiện về cả kỹ thuật và ý tưởng. Tôi có thể giúp bạn **viết file README.md chuyên nghiệp cho GitHub** để bắt đầu thu hút các contributor đầu tiên không?