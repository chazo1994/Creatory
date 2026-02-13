
## 🗺️ Tactical Roadmap (12-Week Sprint)

Targeted for a team of 3–5: **1 Backend/Lead, 1 Frontend/UI, 1 AI/Prompt Specialist, 1 Fullstack/DevOps.**

### Phase 1: Foundation & "The Brain" (Weeks 1–3)

**Objective:** Establish the communication pipes and the primary Agent state.

* **Backend:** Set up `creatory_core` using FastAPI and LangGraph. Implement the **Director Agent** logic.
* **Frontend:** Initialize `creatory_studio` with Next.js 15. Build the Bento Grid layout.
* **Knowledge:** Implement the **File Ingestor** (PDF, Text) to enable the first version of RAG.
* **Milestone:** A creator can upload a file and chat with the Director Agent about its contents.

### Phase 2: Dual-Chat & Research (Weeks 4–6)

**Objective:** Implement the "Contextual Popup" and the first external research tools.

* **Interaction:** Build the **Highlight-to-Ask** frontend logic and the backend **Bridge Injection** service.
* **Research:** Develop and register the **Web Search (Tavily)** and **Scraping (Firecrawl)** MCP servers.
* **UI:** Implement real-time streaming (SSE) for both the main and popup chat windows.
* **Milestone:** A creator can highlight a phrase in their script, search the web via a popup, and inject the findings back into the script.

### Phase 3: The Production Suite (Weeks 7–9)

**Objective:** Empower the Creator with Image, Video, and Audio generation.

* **Creative Tools:** Deploy **MCP Servers** for:
* **Image Gen:** Flux/DALL-E 3.
* **Audio/TTS:** ElevenLabs integration.
* **Video:** Kling or Luma API wrappers.


* **Visual Editor:** Launch the **Node-based Editor** (React Flow) to allow creators to visualize their content pipeline.
* **Milestone:** A user can run a visual workflow that generates an image and a voice-over from a single text prompt.

### Phase 4: Full Orchestration & Polish (Weeks 10–12)

**Objective:** Finalize "Human-in-the-Loop" controls and prepare for Open Source launch.

* **Logic:** Implement **HITL Nodes** (Human-in-the-loop) to pause workflows for user approval.
* **RAG Upgrade:** Finalize the **Hybrid GraphRAG** to ensure consistent brand style across all tools.
* **Library:** Complete the **Media Asset Manager** with preview and "Apply to Project" functionality.
* **Milestone:** **Creatory V0 Public Beta Launch** with a full suite of creative tools.

---

## 👥 III. Team Roles & Success Metrics

### Team Composition

1. **Lead/Backend:** Owns `creatory_core`, Agent logic (LangGraph), and the Bridge service.
2. **Frontend/UI:** Owns `creatory_studio`, React Flow implementation, and SSE streaming.
3. **AI Engineer:** Owns `agents/personas`, System Prompts, RAG tuning, and MCP Tool schemas.
4. **Fullstack/DevOps:** Owns `mcp/servers`, Docker infra, Auth, and Storage logic.

### Success Metrics

* **Efficiency:** Reduce time-to-first-draft for a video script by **60%**.
* **Accuracy:** Contextual Injection must have a **>90%** relevance rate (Agent uses the injected info correctly).
* **Extensibility:** A new MCP tool should take **< 4 hours** to integrate and test.

---

### 🚀 Final Summary

This V0 plan ensures that the **Creatory Framework** is not just a chatbot, but a functional production environment. By leveraging **MCP**, your team stays lean while giving creators access to the latest and greatest AI tools for image, video, and research.

**Would you like me to generate the first `registry.json` manifest to define how the Director Agent should call the Image, Video, and Search tools?**