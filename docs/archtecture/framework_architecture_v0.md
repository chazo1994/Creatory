
## 🏗️ Creatory Technical Design V0 (Full)

### 1. Project Structure (High-Level Overview)

```text
creatory/
├── creatory_core/           # 🧠 The "Brain" (Backend Engine)
│   ├── agents/              # Multi-Agent Orchestration & Personas
│   ├── providers/           # 🔌 [NEW] Provider Abstraction Layer (PAL) for llm and model services (egs: openai, gemini, vllm, ollam,...).
│   ├── api/                 # Interface layer (Versioned via URL routing)
│   ├── db/                  # Persistent data & Vector storage
│   ├── rag/                 # Knowledge retrieval (Hybrid Vector + Graph)
│   ├── services/            # Core business & bridge logic
│   └── main.py              # Application entry point
├── creatory_studio/         # 🎨 The "Workshop" (Frontend Interface)
│   ├── src/
│   │   ├── app/             # Application routing & page structure
│   │   │   ├── chat/        # 💬 The Main Interface (Chat-First UX)
│   │   │   ├── library/     # 📂 (Was Dashboard) Simple Sidebar for History
│   │   │   └── settings/    # ⚙️ Provider & Key Management
│   │   ├── components/      # UI modules (Chat, Workflow Visualizer, Library)
│   │   ├── hooks/           # Reusable frontend logic (SSE, Context Injection)
│   │   ├── lib/             # Utility functions & API clients
│   │   └── store/           # Global state management (Zustand)
├── mcp/                     # 🛠 The "Toolbox" (Model Context Protocol)
│   ├── servers/             # Individual tool servers (Media, Web, Git)
│   ├── registry/            # Tool discovery & manifest management
│   └── sdk/                 # Internal protocol communication layer
├── workflows/               # 🧬 The "DNA" (Shared Blueprints)
│   ├── templates/           # Pre-defined agentic pipeline recipes
│   └── schemas/             # JSON/YAML structure definitions
├── docs/                    # 📚 The "Manual" (Documentation)
├── infra/                   # 🚢 The "Factory" (Deployment & CI/CD)
└── docker-compose.yml       # Full-stack orchestration configuration

```

---

### 2. Module Definitions & Strategic Purpose

#### 🧠 `creatory_core` (Backend Intelligence)

* **`agents/`**: This is the heart of the "Intellectual OS."
* **Purpose:** To host the **Main Director Agent** (Planning/Delegation) and the **Explainer Agent** (Contextual Q&A). It uses stateful logic (LangGraph) to maintain the long-term context of a content project.

* **providers/ (The Hybrid Adaptor)**:
* **Purpose**: Decouples the system from specific AI vendors.

* **`api/`**: The system's gateway.
* **Purpose:** Exposes functionality to the Studio. Versioning (e.g., `/api/v1/`) is implemented at the routing level in code, keeping the folder structure flat and maintainable.


* **`rag/`**: The Hybrid Knowledge Engine.
* **Purpose:** Combines semantic search (Vector) with relational mapping (Graph) to ensure agents understand the Creator’s specific niche, style, and history.


* **`services/`**: The "Glue" Logic.
* **Purpose:** Contains the **Bridge Service** for injecting sub-thread context into the main conversation and the **Workflow Runtime** for converting visual nodes into executable AI tasks.



#### 🎨 `creatory_studio` (Frontend Studio)

* **`app/chat/` (The Chat-First UX)**: The Dual-Interaction interface.
* **Purpose:** Manages the Main Conversation and the **Contextual Popups**. It handles text selection triggers and the "Injection" UI. Also have project management.

* **`components/workflow/`**: The Visual Reasoning Editor.
* **Purpose:** Built on **React Flow**, this allows creators to tweak the "Agentic Workflow" (not code) using a drag-and-drop interface.


* **`store/`**: Session & Context Management.
* **Purpose:** Uses **Zustand** to keep track of active threads, selected text context, and media asset states across the studio panels.



#### 🛠 `mcp` (External Capabilities)

* **`servers/`**: Standardized plugin hosts.
* **Purpose:** To keep the core lean. Capabilities like video generation (Sora) or deep web research (Firecrawl) live here as independent servers that communicate via the Model Context Protocol.


* **`registry/`**: The Tool Catalog.
* **Purpose:** Allows the Director Agent to dynamically "discover" what tools are available without manual code updates.



#### 🧬 `workflows` (Agentic Blueprints)

* **`templates/`**: The "Community Recipes."
* **Purpose:** Stores shareable pipeline definitions (e.g., "YouTube to TikTok Viral Pipeline"). Being at the root level allows these to be easily shared or updated across the ecosystem.



---

### 3. Module Communication Architecture

Creatory uses a specific protocol stack to ensure a professional, production-ready feel:

1. **Streaming (SSE):** `creatory_core` streams AI responses to `creatory_studio` via **Server-Sent Events** to provide that "living" chat experience.
2. **Context Injection (The Bridge):** When a creator "Injects" a sub-thread, a service call within the `core` merges the `Sub-Thread State` into the `Main Thread State` as a system-level update.
3. **Visual Sync (WebSockets):** The Workflow Editor uses WebSockets to show real-time progress as an Agent moves through different nodes in a pipeline.
4. **Tool Execution (MCP):** Agents call tools using **JSON-RPC** over the MCP standard, ensuring any community-built tool can be integrated instantly.

---

### 4. Implementation Notes (Production Readiness)

* **Versioning Strategy:** Implemented via `APIRouter(prefix="/v1")` in the Python code, allowing the project to remain organized while supporting future API iterations.
* **Multi-Modal Pipeline:** The `rag` and `storage` modules are designed to handle not just text, but image metadata and audio transcripts, aligning with the "Creator-First" multi-modal requirement.
* **Human-in-the-Loop:** The `workflow_engine` includes a "Wait" state logic, which stops backend execution until a user signal is received from the Studio.

---

### 🚀 Final Summary

This V0 design provides a scalable foundation for a multi-agent creator platform. It cleanly separates the **AI Reasoning (Core)** from the **User Workspace (Studio)** and provides a standardized way to expand capabilities via **MCP**.

**Would you like me to generate the `docker-compose.yml` file and a basic `.env.example` to help you initialize this exact folder structure on your machine?**