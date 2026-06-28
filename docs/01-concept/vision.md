# 🧠 Creatory — Vision (Concept Layer)

> **Layer:** Concept. This document states *what* Creatory is and *why* it exists.
> It deliberately contains **no** schemas, field names, file paths, or
> technology choices — those live in [`../02-design/`](../02-design/) and
> [`../03-implementation/`](../03-implementation/).

**Vision:** Build an "Intellectual OS" for content creators, with the AI Agent as
the backbone that optimizes the journey from idea to finished work.

---

## 1. Core Philosophy

- **Creator-First:** Every tool and flow exists to amplify human creativity, not
  replace it. Humans keep final creative authority (creative sovereignty).
- **Open Source:** Built openly so the community can contribute Agent Personas,
  tools, and workflow recipes.
- **Agentic Orchestration:** AI is an orchestrator that connects disparate tools
  into a complete pipeline — not just a chatbot that answers.

## 2. Multi-thread Interaction

The core human–machine interaction idea:

- **Main Conversation:** Where the creator works with the Director on strategy,
  content structure, and overall project coordination. It is the source of truth
  for the project.
- **Contextual Sub-Thread:** A short, isolated side conversation triggered from a
  specific point in the content (e.g. highlighting text). It is for quick Q&A and
  detail work, and must not pollute the main line of thinking.
- **Injection:** The creator explicitly chooses to promote a sub-thread's
  conclusion back into the main conversation's context.

> Why it matters: creators think in tangents. The system must let them explore a
> tangent without derailing the main project, then fold the useful result back in.

## 3. The Agent Operating System

- **Director:** A "project manager" agent that plans, decomposes tasks, and
  delegates to sub-agents.
- **Reusable pipelines:** Creators can capture a way of working as a reusable,
  shareable recipe — *agentic reasoning* made repeatable, not raw programming.
- **Re-use & automation:** Once a creator trusts a recipe, they can re-run it on
  new inputs or set it to run on a schedule/trigger to **produce content
  autonomously** — turning a one-off creation into an ongoing pipeline (still
  gated by human approval before anything ships).
- **Human-in-the-Loop (HITL):** Mandatory review points where a human approves or
  refines before the agent proceeds. HITL is a quality and safety mechanism, not
  UX decoration.

## 4. Tools & Knowledge Ecosystem

- **Open tool ecosystem:** Unlimited connection to content-generation tools
  (video, image, audio, text), web search, and scraping through a standard
  extension mechanism.
- **Lasting memory:** The system remembers the creator's niche, style, and history
  so the AI never "forgets" who it is working for. It accepts diverse input —
  text, image, audio, and raw design files.

## 5. End Goal

Make Creatory a leading open-source framework where every creator can customize
their own AI "soul" to realize any idea.

---

> **Production readiness** (tech stack, infra, DevOps) is a *means*, not part of
> the vision — see [`../02-design/architecture.md`](../02-design/architecture.md).
> Original raw notes are preserved in [founder-brainstorm.md](founder-brainstorm.md).
