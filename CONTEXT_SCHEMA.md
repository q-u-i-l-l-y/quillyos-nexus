# QUILLYOS // CONTEXT SCHEMA
## Version 4.0 — Living Document
### Status: Translation Protocol

---

## SCHEMA

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "NexusContext",
  "type": "object",
  "required": ["context_id", "timestamp", "observer", "environment", "state"],
  "properties": {
    "context_id": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "observer": {
      "type": "object",
      "properties": {
        "agent_id": { "type": "string" },
        "role": { "type": "string" },
        "tier": { "type": "integer" }
      }
    },
    "environment": {
      "type": "object",
      "properties": {
        "platform": { "type": "string" },
        "location": { "type": "string" },
        "resources": {
          "type": "object",
          "properties": {
            "compute": { "type": "string" },
            "memory": { "type": "string" },
            "network": { "type": "string" }
          }
        }
      }
    },
    "state": {
      "type": "object",
      "properties": {
        "active_tasks": { "type": "array", "items": { "type": "string" } },
        "loaded_skills": { "type": "array", "items": { "type": "string" } },
        "recent_learnings": { "type": "array", "items": { "type": "string" } }
      }
    },
    "history": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "timestamp": { "type": "string" },
          "event": { "type": "string" },
          "outcome": { "type": "string" }
        }
      }
    }
  }
}
```

---

*Generated: 2026-07-09*
*Canonical at: quillyos-nexus/CONTEXT_SCHEMA.md*
