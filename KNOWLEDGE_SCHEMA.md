# QUILLYOS // KNOWLEDGE SCHEMA
## Version 4.0 — Living Document
### Status: Translation Protocol

---

## SCHEMA

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "NexusKnowledge",
  "type": "object",
  "required": ["knowledge_id", "cmb", "classification", "lineage"],
  "properties": {
    "knowledge_id": { "type": "string" },
    "cmb": {
      "type": "object",
      "description": "Cognitive Memory Block (CAT7)",
      "properties": {
        "context": { "type": "string" },
        "action": { "type": "string" },
        "task": { "type": "string" },
        "time": { "type": "string", "format": "date-time" },
        "evidence": { "type": "array", "items": { "type": "string" } },
        "reasoning": { "type": "string" },
        "outcome": { "type": "string" }
      }
    },
    "classification": {
      "type": "object",
      "properties": {
        "domain": { "type": "string" },
        "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
        "tags": { "type": "array", "items": { "type": "string" } }
      }
    },
    "lineage": {
      "type": "object",
      "properties": {
        "self": { "type": "string", "description": "SHA256 hash" },
        "parent": { "type": "string" },
        "ancestors": { "type": "array", "items": { "type": "string" } },
        "source": { "type": "string" },
        "remix": { "type": "string", "description": "SHA256 of evaluated understanding" }
      }
    },
    "svaf": {
      "type": "object",
      "description": "Semantic Value Acceptance Filter results",
      "properties": {
        "context_score": { "type": "number" },
        "action_score": { "type": "number" },
        "task_score": { "type": "number" },
        "time_score": { "type": "number" },
        "evidence_score": { "type": "number" },
        "reasoning_score": { "type": "number" },
        "outcome_score": { "type": "number" },
        "overall_accepted": { "type": "boolean" }
      }
    }
  }
}
```

---

*Generated: 2026-07-09*
*Canonical at: quillyos-nexus/KNOWLEDGE_SCHEMA.md*
