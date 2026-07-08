# Layer 1 — Evidence

> Filtered, validated, attributed observations. The first gate of truth.

## Purpose

Evidence transforms raw observation into credible information. Not all observations become evidence. Evidence requires:

- **Validation**: Cross-check against known baselines or redundant sensors
- **Attribution**: Clear chain of custody from observation to evidence
- **Classification**: Tagged with type, severity, relevance
- **Deduplication**: Identical or near-identical observations merged

## Schema

```json
{
  "evidence_id": "evd-UUID",
  "parent_observation_ids": ["obs-UUID-1", "obs-UUID-2"],
  "timestamp_created": "ISO-8601",
  "validator": {
    "node_id": "node-UUID",
    "validation_method": "cross_sensor|baseline|human_review|consensus"
  },
  "classification": {
    "type": "financial|health|environmental|security|research",
    "severity": "info|warning|critical",
    "relevance_score": "0.0-1.0"
  },
  "payload": {
    "summary": "human-readable summary",
    "structured_data": {},
    "confidence": "0.0-1.0"
  },
  "audit_trail": [
    {"action": "observed", "timestamp": "...", "node": "..."},
    {"action": "validated", "timestamp": "...", "node": "..."}
  ]
}
```

## Validation Methods

| Method | Description | Use Case |
|--------|-------------|----------|
| cross_sensor | Two+ independent sensors agree | Health vitals, environmental |
| baseline | Deviation from known baseline | Anomaly detection |
| human_review | Human expert verified | Research, legal, medical |
| consensus | Multiple agents agree | Distributed truth |

## Evidence Lifecycle

```
Observation → Validation → Classification → Evidence
     ↓              ↓              ↓
  Raw data    Filtered      Tagged, scored
```

---
*Layer steward: Protocol Council*
*Version: 4.0*
