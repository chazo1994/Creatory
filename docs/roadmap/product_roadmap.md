# 🗺️ CREATORY: VERTICAL SLICE ROADMAP

**Philosophy:** "Ship early, ship complete features."
**Core Tech Stack:** FastAPI, LangGraph, Next.js 15, PostgreSQL (pgvector), Docker.

---

### 📌 Progress Update (Initialization Refactor)

*   [x] Monorepo aligned with `creatory_core/`, `creatory_studio/`, `mcp/`, `workflows/`, `infra/`.
*   [x] Base PAL endpoints added (`catalog`, `test connection`, `routing preview`).
*   [x] Hybrid RAG query endpoint + citation-style response scaffold added.
*   [x] Bridge Injector runtime connected for side-thread -> main-thread context block injection.
*   [x] Starter workflow templates moved to `workflows/templates/`.

---

### 📦 Phase 1: The "Genesis" Slice (Week 1 - 4)
**Goal:** Build the skeleton and **01 complete use-case** (Example: "Create a Podcast Script with a cover image and a sample voiceover"). Users can configure providers directly in the UI.

#### 1. Infrastructure & Core Backend (Week 1)
*   **Architecture Setup:**
    *   [x] Initialize Monorepo: `/creatory_core` (FastAPI), `/creatory_studio` (Next.js), `/workers` (Celery/Arq for background tasks).
    *   [ ] **Provider Abstraction Layer (PAL):** Write a standard interface to switch between providers.
        *   *LLM:* OpenAI, Anthropic, Gemini **vs** Ollama, vLLM, LMStudio.
        *   *Image:* DALL-E 3 **vs** Flux, Stable Diffusion (via A1111/ComfyUI API).
        *   *TTS:* ElevenLabs **vs** Coqui XTTS (Local), OpenVoice.
*   **Database Schema:**
    *   [ ] Design `Projects` table: Each project has its own `settings` (to override global settings if needed).
    *   [ ] Design `Providers` table: Store encrypted API Keys and Endpoint URLs.

#### 2. The "Settings Center" UI (Week 2)
*This is a critical requirement to support flexible providers.*
*   **Global Settings Page:**
    *   [ ] LLM management UI: Dropdown to choose Provider (Ollama/OpenAI...), input Base URL, API Key, Model Name.
    *   [ ] Tools management UI: Toggle Search (Tavily/DDG), Image (Flux/DALL-E).
    *   [ ] **Connection Test:** "Test Connection" button to immediately verify API Key or Local Host status.
*   **Project Settings:**
    *   [ ] Allow overriding default settings per specific project (Example: Project A uses GPT-4, Project B uses local Llama 3 for security).

#### 3. Basic Tools & Circuit Breaker (Week 3)
*   **Tool Integration (Hard-coded logic first):**
    *   [ ] **Search Tool:** Tavily (Cloud) & DuckDuckGo (Free/Local friendly).
    *   [ ] **RAG Lite (Basic):** Upload PDF/Txt -> Chunking -> Vector Store (ChromaDB/PGVector) -> Retrieve top k chunks.
    *   [ ] **Media Tools:** Connect simple Image generation API and TTS.
*   **Safety Mechanism (Circuit Breaker):**
    *   [ ] **Step Limiter:** Middleware in LangGraph counts steps (`recursion_limit`). If > 15 steps -> Automatically stop and report an error.
    *   [ ] **Cost Estimator (Basic):** Basic input/output token counting, warn if exceeding threshold (for paid APIs).

#### 4. The "Genesis" Flow (Week 4 - Demo Time)
*   **Main Chat Interface:**
    *   [ ] Basic Chat UI: Show Message History, Markdown rendering.
    *   [ ] **Context Sidebar:** Show list of files uploaded into the Project (RAG).
*   **End-to-End Test:**
    *   [ ] User creates Project "Podcast AI".
    *   [ ] User config Settings: LLM = Ollama (Llama 3), Image = Flux.
    *   [ ] User chat: "Please research the topic of AI Agents from the PDF file I just uploaded, write a podcast script, and create a cover image."
    *   [ ] **Result:** The system returns Text (Script) + Image (Cover) + Audio (30s Intro) in the same chat frame.

---

### 🧱 Phase 2: The "Dual-Stream" & Deep Context (Week 5 - 8)
**Goal:** Upgrade the UX with "Contextual Chat" and complete the RAG implementation.

#### 1. Dual-Stream UI/UX (Week 5-6)
*   **Split View Interface:**
    *   [ ] Split layout: Main Artifact (Article/Script) on the left - Chat/Agent on the right.
    *   [ ] **Highlight Action:** Highlight text on the left -> Show tooltip "Ask AI" or "Refine".
*   **Sub-Thread Architecture:**
    *   [ ] Create a separate child `Thread` for each "Ask AI".
    *   [ ] **Bridge Injection Logic:** "Apply to Main" button in the sub-flow -> Call LLM to synthesize changes and update the main content on the left.

#### 2. Advanced RAG & Knowledge (Week 7)
*   **Knowledge Base Upgrade:**
    *   [ ] Support multiple formats: Docx, MD, Youtube URL (extract transcript).
    *   [ ] **Source Citation:** When the Agent answers from RAG, it must show numbers [1], [2] linking back to the original text passages in the document.
    *   [ ] **NotebookLM Style:** "Audio Overview" feature - Summarize the entire document into a conversational Audio file (leveraging the TTS tool built in Phase 1).

#### 3. Local-First Optimization (Week 8)
*   **Offline Mode:**
    *   [ ] Package a Docker Compose profile `local-only`: Automatically pull Ollama, Qdrant/Chroma, Stable Diffusion container.
    *   [ ] Test performance when running the full stack locally.

---

### 🛠️ Phase 3: Workflows & Visualization (Week 9 - 12)
**Goal:** Allow users to intervene in the Agent’s reasoning process (customizable logic).

#### 1. Code-based Workflows (YAML Templates) (Week 9-10)
*   **Template Engine:**
    *   [ ] Define a YAML structure for Workflows:
        ```yaml
        name: "Youtube Short Generator"
        steps:
          - research: { source: "google_trends", topic: "{input}" }
          - script: { model: "gpt-4", style: "viral" }
          - image: { model: "flux", prompt: "{script.scene_1}" }
        ```
    *   [ ] **Workflow Runner:** Backend parses the YAML file and builds a Dynamic LangGraph based on that structure.
*   **Community Library:**
    *   [ ] Create a repo containing sample YAML files for users to import (e.g., "Blog SEO Writer", "Email Responder").

#### 2. Visual Viewer (Read-only) (Week 11)
*   **Pipeline Visualization:**
    *   [ ] Integrate React Flow.
    *   [ ] **Live Tracing:** When the Agent runs a YAML/Template file, the UI highlights nodes in real time (running Research step -> running Writing step...).
    *   [ ] *Note:* View-only, no drag-and-drop editing yet to avoid complexity.

#### 3. Advanced Management & Analytics (Week 12)
*   **Dashboard:**
    *   [ ] Token usage statistics per Project.
    *   [ ] Detailed Agent error logs.
*   **Release Beta v0.9:**
    *   [ ] Full Documentation.
    *   [ ] Installation tutorial video: Local vs Cloud.

---

### ✅ Contributor Checklist

To ensure progress, you can create GitHub Issues based on this checklist:

**Backend (Python/FastAPI):**
- [ ] Implement `LLMProviderFactory` (Support OpenAI, Ollama interfaces).
- [ ] Implement `ToolBase` class (Search, ImageGen, TTS).
- [ ] Setup LangGraph State Checkpointer (Postgres).
- [ ] Build `CircuitBreakerMiddleware` for infinite loop prevention.
- [ ] Implement `YAMLWorkflowParser`.

**Frontend (Next.js/React):**
- [ ] Build `SettingsPage` with encrypted local storage for API keys (or send to backend vault).
- [ ] Build `ProjectDashboard` (Grid view).
- [ ] Implement `DualStreamLayout` (Resizable panes).
- [ ] Build `ChatInterface` with Multi-modal rendering (Display Image/Audio cards).
- [ ] Implement `ReactFlow` viewer for Agent state visualization.

**DevOps/AI:**
- [ ] Dockerize `Ollama` service setup script.
- [ ] Optimize `pgvector` indexing for RAG.
- [ ] Create default prompts/personas for "Main Director Agent".

---

With this Roadmap, you solve the **"chicken-and-egg"** problem:
1.  **Within the first month:** You have a usable product (Vertical Slice).
2.  **Open Source Friendly:** Support Local LLM/Tools immediately.
3.  **Scalable:** The Project structure and Settings UI lay the foundation for future expansion.
