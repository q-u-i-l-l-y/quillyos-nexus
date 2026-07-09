# QUILLYOS // DECISION SCHEMA
## Version 4.0 — Living Document
### Status: Translation Protocol

---

## SCHEMA

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "NexusDecision",
  "type": "object",
  "required": ["decision_id", "observer", "evidence", "context", "principles",
               "options", "impact", "choice", "timestamp"],
  "properties": {
    "decision_id": { "type": "string" },
    "observer": {
      "type": "object",
      "properties": {
        "agent_id": { "type": "string" },
        "role": { "type": "string" }
      }
    },
    "evidence": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "evidence_id": { "type": "string" },
          "source": { "type": "string" },
          "relevance": { "type": "number" }
        }
      }
    },
    "context": { "type": "string" },
    "principles": {
      "type": "array",
      "items": { "type": "string", "description": "References to ETHICS.md principles" }
    },
    "options": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "option_id": { "type": "string" },
          "description": { "type": "string" },
          "pros": { "type": "array", "items": { "type": "string" } },
          "cons": { "type": "array", "items": { "type": "string" } }
        }
      }
    },
    "impact": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "stakeholder": { "type": "string" },
          "effect": { "type": "string" },
          "severity": { "type": "string", "enum": ["low", "medium", "high", "critical"] }
        }
      }
    },
    "choice": {
      "type": "object",
      "properties": {
        "option_id": { "type": "string" },
        "justification": { "type": "string" },
        "confidence": { "type": "number" }
      }
    },
    "timestamp": { "type": "string", "format": "date-time" },
    "outcome": {
      "type": "object",
      "properties": {
        "status": { "type": "string", "enum": ["pending", "implemented", "reversed"] },
        "result": { "type": "string" },
        "lessons": { "type": "array", "items": { "type": "string" } }
      }
    }
  }
}
```

---

*Generated: 2026-07-09*
*Canonical at: quillyos-nexus/DECISION_SCHEMA.md*
