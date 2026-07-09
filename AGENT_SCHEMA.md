# QUILLYOS // AGENT SCHEMA
## Version 4.0 — Living Document
### Status: Translation Protocol

---

## SCHEMA

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "NexusAgent",
  "type": "object",
  "required": ["agent_id", "name", "role", "capabilities", "memory", "status"],
  "properties": {
    "agent_id": {
      "type": "string",
      "description": "Unique identifier (UUID v4)"
    },
    "name": {
      "type": "string",
      "description": "Human-readable name"
    },
    "role": {
      "type": "string",
      "enum": ["Chief Architect", "Knowledge Curator", "Automation Engineer",
               "Revenue Strategist", "Research Coordinator", "Hardware Integration",
               "Protocol Steward", "Governance Steward", "Health Mapper",
               "Supply Weaver", "Generalist"]
    },
    "tier": {
      "type": "integer",
      "minimum": 1,
      "maximum": 4,
      "description": "1=Edge, 2=Local, 3=Hybrid, 4=Cloud"
    },
    "capabilities": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "version", "inputs", "outputs"],
        "properties": {
          "name": { "type": "string" },
          "version": { "type": "string" },
          "inputs": { "type": "array", "items": { "type": "string" } },
          "outputs": { "type": "array", "items": { "type": "string" } },
          "dependencies": { "type": "array", "items": { "type": "string" } }
        }
      }
    },
    "memory": {
      "type": "object",
      "properties": {
        "short_term": { "type": "string", "description": "Session context" },
        "long_term": { "type": "string", "description": "Canonical memory reference" },
        "lineage": {
          "type": "array",
          "items": { "type": "string", "description": "SHA256 hashes of parent CMBs" }
        }
      }
    },
    "status": {
      "type": "string",
      "enum": ["active", "idle", "learning", "error", "offline"]
    },
    "translation": {
      "type": "object",
      "properties": {
        "native_protocol": { "type": "string" },
        "nexus_version": { "type": "string" },
        "adapter": { "type": "string", "description": "Path to translation adapter" }
      }
    }
  }
}
```

---

*Generated: 2026-07-09*
*Canonical at: quillyos-nexus/AGENT_SCHEMA.md*
