# Reference Policy

## Purpose

This document defines how external repositories may be used as architecture references in Creatory research work.

The immediate use case is `openai/codex`, but the same rules should apply to similar reference repos unless a stricter rule is documented elsewhere.

---

## Default Rule

External reference repositories are for **reading, analysis, note-taking, and architectural comparison only**.

They are **not** part of the Creatory codebase unless the team explicitly decides otherwise through a documented legal and architectural review.

---

## Allowed

- Clone a reference repo into a gitignored folder such as `.references/`.
- Read source code, docs, schemas, and module layouts for reverse-engineering.
- Use `rg`, local code search, and notes to understand runtime flow and architecture.
- Write internal research notes, RFCs, diagrams, and mapping documents derived from those observations.
- Re-implement an idea in Creatory from first principles when it fits the product architecture.

---

## Not Allowed

- Import packages, crates, modules, or source files from a reference repo into Creatory runtime code.
- Vendor or copy the reference repo into `creatory_core/`, `creatory_studio/`, `mcp/`, `workflows/`, or other production paths.
- Add the reference repo as a build dependency, runtime dependency, submodule, or hidden bootstrap dependency.
- Copy-paste substantial upstream code into Creatory without explicit legal and architecture approval.
- Blur the boundary between “research artifact” and “production artifact”.

---

## Required Hygiene

- Keep reference repositories in `.references/` or outside the main repo.
- Keep `.references/` gitignored.
- When a research note relies strongly on an upstream design, cite the upstream repo and the specific file or document.
- When a Creatory implementation borrows a pattern, document the reasoning in an RFC, design note, or code comment when appropriate.
- Prefer re-designing concepts in Creatory terms instead of mirroring upstream structure mechanically.

---

## Codex-Specific Note

`openai/codex` is approved as a **reference-only architecture source** for:

- runtime layering
- thread/turn/event flow
- tool and MCP orchestration patterns
- context assembly patterns
- multi-agent topology patterns

It is not approved as a direct implementation dependency for Creatory by default.
