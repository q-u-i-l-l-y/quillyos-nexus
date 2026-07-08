# Relationship Schema

> How entities connect in the Nexus knowledge graph

## Relationship Types

| Type | Direction | Description |
|------|-----------|-------------|
| depends_on | A → B | A cannot function without B |
| enables | A → B | A makes B possible |
| contains | A → B | A physically or logically contains B |
| references | A → B | A cites or uses B |
| replaces | A → B | A supersedes B (B deprecated) |
| reports_to | A → B | A sends data/status to B |
| peer_of | A ↔ B | A and B are equivalent nodes |
| conflicts_with | A ↔ B | A and B contain contradictory information |

## Schema

```json
{
  "relationship_id": "rel-UUID",
  "from_entity": "entity-UUID-A",
  "to_entity": "entity-UUID-B",
  "type": "depends_on|enables|contains|references|replaces|reports_to|peer_of|conflicts_with",
  "strength": "0.0-1.0",
  "evidence": ["evd-UUID-1"],
  "created": "ISO-8601",
  "steward": "node-UUID"
}
```

## Example: phone_bootstrap → Nexus

```json
{
  "relationship_id": "rel-001",
  "from_entity": "entity-node-revenue-01",
  "to_entity": "entity-protocol-001",
  "type": "contains",
  "strength": 1.0,
  "evidence": ["evd-legacy-audit-001"],
  "created": "2026-07-08T12:58:00Z",
  "steward": "node-hub-01"
}
```

## Query Patterns

- "What depends on entity X?" → Find all `depends_on` where `to_entity = X`
- "What does entity X enable?" → Find all `enables` where `from_entity = X`
- "What conflicts exist?" → Find all `conflicts_with` relationships
- "What is the dependency chain for milestone Y?" → Recursive `depends_on` traversal

---
*Relationship steward: Knowledge Curator*
*Version: 4.0*
