## Detailed Conceptual Blueprint (Creator-First)

This blueprint is strictly aligned with your vision of a **Multi-Agent "Intellectual OS"** for creators.

### 1. The Core Architecture (Stateful Orchestration)

The system operates as a **Stateful Orchestration** engine. Unlike static chatbots, Creatory maintains a living "State" of the creative project.

* **Main Director Agent (The Brain):** Acts as the primary touchpoint. It performs **Intention Decoding**—taking a vague creative idea and breaking it into a structured plan (Planning) and executing it via sub-agents.
*   **Hybrid AI Engine (The Muscle):**
    *   **Provider Abstraction:** The system is model-agnostic. It can run on **Local LLMs** (Ollama/vLLM) for privacy/zero-cost or switch to **Cloud APIs** (OpenAI/Anthropic) for complex reasoning on the fly.
    *   **Strategic Routing:** The Director Agent can decide to use a "Cheap Model" (Local) for drafting and a "Smart Model" (Cloud) for final polishing.

### 2. Innovation: Dual-Stream Interaction

Creatory introduces a "Human-in-the-Loop" multitasking interface:

* **Main Stream (Primary Thread):** Where the long-form content (script, video structure, marketing plan) is forged.
* **Contextual Sub-Streams (Popups):**
* **Trigger:** Highlight any text/element to ask "Quick Questions" or add "Comments."
* **Isolation:** These sub-chats use an isolated context. The Main Director isn't distracted by these "side-quests" unless invited.
* **Bridge Injector:** A dedicated mechanism to extract conclusions or data blocks from a sub-chat and **Inject** them back into the Main Stream context as verified info.



### 3. Agentic Workflow & Node System
Creatory prioritizes **Logical Precision** over just graphical interfaces:

* **Chat-based Workflow:** The Agent builds the pipeline automatically based on chat instructions.
*   **Code-First Templates (YAML/JSON):** Complex workflows are defined in clean, version-controllable templates. This allows the community to share "Recipes" (e.g., "Viral Short Video Pipeline") easily.
*   **Visual Viewer (Read-only):** A real-time graph visualization (React Flow) creates transparency, showing exactly which step the Agent is executing.
* **Agentic, Not just Code:** Nodes represent **Agent Personas** or **MCP Tools** or code functions,...
* **Human-in-the-loop Node:** A mandatory "stop" node where the creator must approve or tweak output before the pipeline proceeds, waiting for user confirmation via the UI. Event human in the loop can be designed by user / creator via Director Agent.
*   *(Future Phase)* **Node-based Editor:** A drag-and-drop area for deep tuning (Planned for later phases).

### 4. Memory & Knowledge (Hybrid RAG)

The system ensures the AI never "forgets" the creator's unique style:

* **Vector Database:** Stores raw content (PDFs, links, transcripts).
* **Graph Database:** Maps relationships between concepts, recurring characters, and style preferences.
* **Input Diversity:** Supports text, images, audio, and raw design files as context.

### 5. Tools & MCP (Model Context Protocol)

To ensure infinite extensibility by the open-source community:

* **Media Suite:** Integration with top-tier AI engines (Video/Image/Audio/Text).
* **Web Suite:** Real-time trend analysis via scraping and search engines.
* **Production Suite:** Integrated Git and Docker APIs to automate the deployment of final content.

### 6. Production-Ready Infrastructure

* **Frameworks:** Built on **FastAPI** + **LangGraph** (Backend) and **Next.js** (Frontend).
* **Database:** **PostgreSQL** (User/Session data) + **pgvector** (Long-term memory).
* **DevOps:** Full `docker-compose` setup, Git pre-commit hooks for quality control, and built-in User/Auth management.

### 7. Safety & Governance (The Guardrails)
To make Agentic AI production-ready and cost-effective:

*   **Circuit Breaker:** A dedicated middleware that monitors the Agent's loop. It automatically halts execution if the Agent exceeds a step limit (preventing infinite loops) or a token budget.
