# QUILLYOS // REASONING SCHEMA
## Version 4.0 — Living Document
### Status: Translation Protocol

---

## SCHEMA

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "NexusReasoning",
  "type": "object",
  "required": ["reasoning_id", "premises", "inference", "confidence", "tests"],
  "properties": {
    "reasoning_id": { "type": "string" },
    "premises": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "statement": { "type": "string" },
          "source": { "type": "string" },
          "evidence_id": { "type": "string" }
        }
      }
    },
    "inference": {
      "type": "object",
      "properties": {
        "conclusion": { "type": "string" },
        "method": { "type": "string" },
        "framework": { "type": "string" }
      }
    },
    "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
    "tests": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "test_id": { "type": "string" },
          "method": { "type": "string" },
          "status": { "type": "string", "enum": ["pending", "passed", "failed", "inconclusive"] },
          "result": { "type": "string" }
        }
      }
    },
    "alternatives": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "conclusion": { "type": "string" },
          "confidence": { "type": "number" }
        }
      }
    }
  }
}
```

---

*Generated: 2026-07-09*
*Canonical at: quillyos-nexus/REASONING_SCHEMA.md*
