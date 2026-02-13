## Detailed Conceptual Blueprint (Creator-First)

This blueprint is strictly aligned with your vision of a **Multi-Agent "Intellectual OS"** for creators.

### 1. The Core Architecture (Stateful Orchestration)

The system operates as a **Stateful Orchestration** engine. Unlike static chatbots, Creatory maintains a living "State" of the creative project.

* **Main Director Agent (The Brain):** Acts as the primary touchpoint. It performs **Intention Decoding**—taking a vague creative idea and breaking it into a structured plan (Planning) and executing it via sub-agents.

### 2. Innovation: Dual-Stream Interaction

Creatory introduces a "Human-in-the-Loop" multitasking interface:

* **Main Stream (Primary Thread):** Where the long-form content (script, video structure, marketing plan) is forged.
* **Contextual Sub-Streams (Popups):**
* **Trigger:** Highlight any text/element to ask "Quick Questions" or add "Comments."
* **Isolation:** These sub-chats use an isolated context. The Main Director isn't distracted by these "side-quests" unless invited.
* **Bridge Injector:** A dedicated mechanism to extract conclusions or data blocks from a sub-chat and **Inject** them back into the Main Stream context as verified info.



### 3. Agentic Workflow & Node System

Creatory distinguishes between **Natural Language** and **Visual Precision**:

* **Chat-based Workflow:** The Agent builds the pipeline automatically based on chat instructions.
* **Node-based Editor (Visual Programming):** A dedicated area for deep tuning.
* **Agentic, Not Code:** Nodes represent **Agent Personas** or **MCP Tools**, not raw code functions.
* **Human-in-the-loop Node:** A mandatory "stop" node where the creator must approve or tweak output before the pipeline proceeds.



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
