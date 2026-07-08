# Entity Template

> Canonical entity definition for the Nexus knowledge graph

## Schema

```json
{
  "entity_id": "entity-UUID",
  "entity_type": "agent|device|service|protocol|document|revenue_stream|research_topic",
  "name": "human-readable name",
  "description": "brief description",
  "status": "active|planned|deprecated|archived",
  "created": "ISO-8601",
  "modified": "ISO-8601",
  "steward": "node-UUID or human-id",
  "context_matrix": "matrix-001|matrix-002|matrix-003|...",
  "attributes": {},
  "relationships": [
    {"target": "entity-UUID", "type": "depends_on|enables|contains|references|replaces"}
  ],
  "evidence": ["evd-UUID-1", "evd-UUID-2"],
  "translations": ["trn-UUID-1", "trn-UUID-2"]
}
```

## Example: Spoke-Revenue Node

```json
{
  "entity_id": "entity-node-revenue-01",
  "entity_type": "device",
  "name": "Spoke-Revenue Primary Node",
  "description": "Phone-based business automation platform running Termux",
  "status": "active",
  "created": "2026-01-01T00:00:00Z",
  "modified": "2026-07-08T12:58:00Z",
  "steward": "human-quilly",
  "context_matrix": "matrix-001",
  "attributes": {
    "hardware": "Android phone",
    "os": "Termux",
    "python_scripts": 24,
    "json_memory_files": 25,
    "primary_function": "service_arbitrage"
  },
  "relationships": [
    {"target": "entity-revenue-001", "type": "contains"},
    {"target": "entity-node-hub-01", "type": "reports_to"}
  ]
}
```

## Legacy Mapping: phone_bootstrap → Nexus

The `phone_bootstrap` system contains 24 Python scripts and 25 JSON memory files. These map to Nexus entities as follows:

| phone_bootstrap Component | Nexus Entity Type | Migration Action |
|---------------------------|-------------------|------------------|
| Python scripts (24) | `agent` entities | Extract functions, create skill manifests |
| JSON memory files (25) | `document` entities | Convert to structured entity definitions |
| config.reference.json | `protocol` entity | Elevate to Layer 2 context |
| memory_agent_context.json | `agent` entity | Merge into entity attributes |

### Migration Steps

1. Archive `phone_bootstrap` in `picoclaw-dev/archive/`
2. Read `config.reference.json` → create `entity-protocol-001`
3. Read `memory_agent_context.json` → create `entity-agent-001`
4. Map each Python script → `entity-skill-XXX` with manifest
5. Map each JSON memory file → `entity-memory-XXX` with context

---
*Entity steward: Knowledge Curator*
*Version: 4.0*
