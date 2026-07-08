# Layer 4 — Consensus

> Cross-agent validated knowledge. The canonical layer.

## Purpose

Consensus is the highest layer of the protocol stack. Knowledge reaches consensus when:

1. Multiple independent agents have translated the same context
2. Their translations agree on core facts
3. Disagreements are documented and flagged for review
4. A governance decision records the validated state

## Consensus Schema

```json
{
  "consensus_id": "cns-UUID",
  "parent_translation_ids": ["trn-UUID-1", "trn-UUID-2"],
  "timestamp_validated": "ISO-8601",
  "participating_nodes": ["node-UUID-1", "node-UUID-2", "node-UUID-3"],
  "agreement_score": "0.0-1.0",
  "canonical_state": {
    "facts": ["validated fact 1", "validated fact 2"],
    "uncertainties": ["disputed point 1"],
    "actions": ["recommended action 1"]
  },
  "governance_record": {
    "decision_type": "merge|override|flag_for_review|archive",
    "steward": "node-UUID or human-id",
    "rationale": "human-readable reasoning"
  }
}
```

## Consensus Rules

1. **No unilateral consensus**: Minimum 2 independent nodes must agree
2. **Disagreement is data**: Disputed points are recorded, not suppressed
3. **Consensus is versioned**: New evidence can invalidate old consensus
4. **Git is the constitution**: All consensus records are committed to version control
5. **Hub nodes arbitrate**: When spokes disagree, the Hub node decides

## Mesh Governance

```
Spoke nodes propose → Hub nodes validate → Consensus layer records
         ↓                    ↓                    ↓
    Local evidence       Cross-reference       Canonical truth
```

---
*Layer steward: Protocol Council*
*Version: 4.0*
