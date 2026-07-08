# Layer 2 — Context

> Evidence placed in architectural, temporal, and relational context.

## Purpose

Context is where meaning emerges. Evidence without context is just data. Context provides:

- **Architectural placement**: Where does this fit in the system?
- **Temporal placement**: What happened before and after?
- **Relational placement**: What entities does this connect to?
- **Strategic placement**: How does this affect mission objectives?

## Schema

```json
{
  "context_id": "ctx-UUID",
  "parent_evidence_ids": ["evd-UUID-1", "evd-UUID-2"],
  "timestamp_created": "ISO-8601",
  "context_matrix": {
    "mission": "Which mission objective does this relate to?",
    "milestone": "Which milestone is affected?",
    "domain": "revenue|health|hardware|research|governance",
    "dependencies": ["ctx-UUID-3", "ctx-UUID-4"],
    "blockers": ["ctx-UUID-5"],
    "opportunities": ["ctx-UUID-6"]
  },
  "narrative": "human-readable contextual narrative",
  "entity_map": {
    "primary_entities": ["entity-UUID-1"],
    "related_entities": ["entity-UUID-2", "entity-UUID-3"],
    "relationships": [
      {"from": "entity-1", "to": "entity-2", "type": "depends_on|enables|blocks|references"}
    ]
  }
}
```

## Context Matrices

Context matrices are pre-built context containers for recurring domains. See `contexts/matrices/`.

| Matrix | Domain | Purpose |
|--------|--------|---------|
| matrix-001 | Revenue & Finance | Service arbitrage, real estate, digital products |
| matrix-002 | Hardware & ENDS | Device modules, sensors, manufacturing |
| matrix-003 | Research & Knowledge | Metamaterials, quantum, agent coordination |

---
*Layer steward: Protocol Council*
*Version: 4.0*
