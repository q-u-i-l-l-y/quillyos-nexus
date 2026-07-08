# Consensus Records

> Validated mesh decisions and canonical knowledge states

## Purpose

This directory contains governance decisions, consensus records, and validated knowledge states. Every file here represents agreement across multiple nodes.

## Record Format

```json
{
  "consensus_id": "cns-UUID",
  "title": "human-readable title",
  "timestamp": "ISO-8601",
  "participating_nodes": ["node-UUID-1", "node-UUID-2"],
  "agreement_score": 0.95,
  "decision_type": "merge|override|flag_for_review|archive",
  "canonical_state": {},
  "rationale": "human-readable reasoning",
  "steward": "node-UUID"
}
```

## Decision Types

| Type | Description |
|------|-------------|
| merge | Combine multiple translations into one canonical state |
| override | Hub node overrules a spoke proposal |
| flag_for_review | Insufficient agreement — needs more evidence |
| archive | Knowledge is outdated but preserved for history |

## Active Records

| Consensus ID | Title | Status | Steward |
|--------------|-------|--------|---------|
| cns-001 | Master Vision Brief v4.0 adoption | Active | node-hub-01 |
| cns-002 | quillyos-nexus repo creation | Active | node-hub-01 |

## Governance Principles

1. Git is the constitution — all decisions are committed
2. No decision without at least 2 agreeing nodes
3. Disagreement is recorded, not suppressed
4. Hub nodes arbitrate when spokes disagree
5. All records are public and auditable

---
*Consensus steward: Governance Steward*
*Version: 4.0*
