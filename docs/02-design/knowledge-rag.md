# 📚 Knowledge Layer — Hybrid RAG (Design Layer)

> **Layer:** Design (normative). Traces up to
> [`../01-concept/business-requirements.md`](../01-concept/business-requirements.md)
> FR-07. Data contracts in [data-model.md](data-model.md) §7.

## Goals

- The system MUST support **Hybrid RAG** at the architectural level: vector
  (semantic) + graph (relational) retrieval.
- Retrieval SHOULD return **citation-capable** context (answers can point back to
  source passages).
- Input SHOULD be diverse: text, image metadata, audio/transcript, links, raw
  documents.

## Components

| Component | Responsibility |
| --- | --- |
| **Vector store** | Semantic search over chunked source content. |
| **Graph store** | Relationships between concepts, recurring entities, and the creator's style preferences (the "brand voice"). |
| **Ingestion** | Normalizes diverse inputs into sources → chunks → embeddings. |

## Rules

- Retrieval results SHOULD carry source references usable for inline citations
  (e.g. `[1]`, `[2]`).
- The graph layer MAY initially live inside PostgreSQL and migrate to a dedicated
  graph DB later — see [data-model.md](data-model.md) §7 (`concept_nodes`,
  `concept_edges`).
