# QUILLYOS // TASK SCHEMA
## Version 4.0 — Living Document
### Status: Translation Protocol

---

## SCHEMA

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "NexusTask",
  "type": "object",
  "required": ["task_id", "requester", "capability", "parameters", "priority"],
  "properties": {
    "task_id": { "type": "string" },
    "requester": {
      "type": "object",
      "properties": {
        "agent_id": { "type": "string" },
        "role": { "type": "string" }
      }
    },
    "capability": { "type": "string", "description": "Name of requested skill" },
    "parameters": { "type": "object" },
    "priority": {
      "type": "integer",
      "minimum": 1,
      "maximum": 5,
      "description": "1=Critical, 5=Background"
    },
    "deadline": { "type": "string", "format": "date-time" },
    "constraints": {
      "type": "array",
      "items": { "type": "string" }
    },
    "dependencies": {
      "type": "array",
      "items": { "type": "string", "description": "task_ids that must complete first" }
    }
  }
}
```

---

*Generated: 2026-07-09*
*Canonical at: quillyos-nexus/TASK_SCHEMA.md*
