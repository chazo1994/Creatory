## 📋 Business Requirements Document (BRD)

### 1. Vision Statement

To build an open-source "Intellectual OS" that empowers content creators to move from **Idea to Execution** using a multi-agent AI system. Creatory bridges the gap between raw imagination and professional production by providing an environment where AI manages the heavy lifting while the human retains creative sovereignty.

### 2. Core Functional Requirements (FR)

#### A. Interaction & Orchestration

| ID | Feature | Description | Priority |
| --- | --- | --- | --- |
| **FR-01** | **Main Director Agent** | Stateful "Project Manager" agent that decodes intent, plans tasks, and delegates to specialized sub-agents. | P0 |
| **FR-02** | **Dual-Stream Chat** | Parallel interaction: A **Main Canvas** for the project and **Contextual Popups** for isolated, highlight-based Q&A. | P0 |
| **FR-03** | **Bridge Injection** | Logic to summarize and "promote" insights/data from an isolated popup thread directly into the Main Project context. | P0 |
| **FR-04** | **Agentic Node Editor** | A drag-and-drop visual interface (React Flow) to design and debug high-level Agent logic and tool chains. | P1 |
| **FR-04A** | **Provider Settings Center (PAL)** | UI/API to manage provider catalog, test provider connectivity, and preview local-vs-cloud routing strategy. | P0 |

#### B. The Creator Toolset (MCP-Driven)

| ID | Module | Requirement | Priority |
| --- | --- | --- | --- |
| **FR-05** | **Research Suite** | Real-time **Web Search** (Tavily) and **Deep Web Scraping** (Firecrawl) to fuel content with current trends and facts. | P0 |
| **FR-06** | **Media Gen Suite** | One-click generation for **Images** (Flux), **Videos** (Kling/Sora API), and **Audio/TTS** (ElevenLabs) via MCP. | P1 |
| **FR-07** | **Hybrid RAG** | Memory system using Vector (semantic) and Graph (relational) data to maintain a "Brand Voice" and "Creator Knowledge." | P1 |
| **FR-08** | **Asset Library** | A centralized manager to preview, version, and "inject" AI-generated media into workflows or scripts. | P2 |

### 3. Non-Functional Requirements (NFR)

* **Extensibility:** Tools must be added via **Model Context Protocol (MCP)** servers without modifying the core orchestrator logic.
* **Production Readiness:** Full **Dockerized** environments with CI/CD support for small-team deployments.
* **Latency:** Streaming responses (SSE) for text and real-time status updates for media rendering.
* **Safety:** Integrated **Human-in-the-Loop (HITL)** checkpoints for all creative tool outputs.
* **Security:** Provider credentials must not be hardcoded in source and require a secure management path.
