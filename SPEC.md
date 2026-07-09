# QUILLYOS // NEXUS SPECIFICATION
## Version 4.0 — Living Document
### Status: Translation Protocol

---

## OVERVIEW

The Nexus Protocol is a structured representation of reality designed for
machine-to-machine and human-to-machine communication. It replaces unstructured
conversation with structured, versioned, cross-referenceable information.

---

## DESIGN GOALS

1. **Model Agnostic** — Any AI system can consume and produce Nexus documents
2. **Human Readable** — Humans can read, write, and review Nexus documents
3. **Machine Parseable** — Nexus documents are valid JSON with strict schemas
4. **Versioned** — Every document has a version and lineage
5. **Cross-Referenceable** — Every document references its sources and dependencies
6. **Self-Describing** — The protocol describes itself

---

## CORE CONCEPTS

### Cognitive Memory Block (CMB)

The atomic unit of Nexus knowledge. Defined by the CAT7 schema:

```json
{
  "context": "The situation in which the observation was made",
  "action": "What was done or observed",
  "task": "The capability request that triggered the action",
  "time": "ISO 8601 timestamp",
  "evidence": "Supporting data, references, measurements",
  "reasoning": "The inference chain that led to the conclusion",
  "outcome": "The result or state after the action"
}
```

### Semantic Value Acceptance Filter (SVAF)

Before a CMB is accepted into canonical memory, each field is evaluated:

| Field | Filter | Threshold |
|-------|--------|-----------|
| context | Completeness | ≥ 3 contextual dimensions |
| action | Specificity | No vague verbs |
| task | Traceability | Links to capability request |
| time | Precision | ISO 8601, no relative time |
| evidence | Verifiability | ≥ 1 primary source |
| reasoning | Validity | Logical, no fallacies |
| outcome | Measurability | Quantified where possible |

### Inter-Agent Lineage

Every CMB carries a lineage chain:

```json
{
  "lineage": {
    "self": "sha256_hash_of_this_block",
    "parent": "sha256_hash_of_predecessor",
    "ancestors": ["hash_1", "hash_2", "..."],
    "source": "origin_repository_or_agent",
    "remix": "sha256_hash_of_role_evaluated_understanding"
  }
}
```

The `remix` field is critical: it stores only the agent's evaluated understanding
of the source, never the raw source signal. This prevents information pollution
and ensures that every agent in the mesh adds value, not noise.

---

## TRANSPORT

Nexus documents are transported via:
1. **Git** — canonical memory, versioned, permanent
2. **MCP** — real-time tool interoperability
3. **A2A** — agent-to-agent communication
4. **HTTP/JSON** — external system integration

---

*Generated: 2026-07-09*
*Canonical at: quillyos-nexus/SPEC.md*
