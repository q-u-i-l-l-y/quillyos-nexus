# Layer 0 — Observation

> Raw sensor input. Unfiltered. Timestamped. Attributed.

## Purpose

The observation layer captures reality before interpretation. Every observation is:

- **Timestamped**: When did this occur?
- **Attributed**: Who or what observed it?
- **Raw**: No filtering, no classification, no judgment
- **Structured**: Machine-readable format

## Schema

```json
{
  "observation_id": "obs-UUID",
  "timestamp": "ISO-8601",
  "source": {
    "node_id": "node-UUID",
    "node_type": "Spoke-Compute|Spoke-Health|Spoke-Data|...",
    "sensor": "camera|microphone|thermal|biometric|financial_api|..."
  },
  "payload": {
    "type": "image|audio|numeric|text|event|transaction",
    "data": "<base64 or raw value>",
    "unit": "celsius|dB|USD|bpm|..."
  },
  "metadata": {
    "location": "optional GPS or logical location",
    "confidence": "0.0-1.0 if applicable",
    "raw_hash": "sha256 of raw data for integrity"
  }
}
```

## Example: Financial Observation

```json
{
  "observation_id": "obs-2026-07-08-001",
  "timestamp": "2026-07-08T12:58:00Z",
  "source": {
    "node_id": "spoke-revenue-01",
    "node_type": "Spoke-Revenue",
    "sensor": "financial_api"
  },
  "payload": {
    "type": "transaction",
    "data": {"asset": "ETH", "price_usd": 2850.42, "volume_24h": 12400000000},
    "unit": "USD"
  }
}
```

## Example: Health Observation

```json
{
  "observation_id": "obs-2026-07-08-002",
  "timestamp": "2026-07-08T12:58:00Z",
  "source": {
    "node_id": "spoke-health-01",
    "node_type": "Spoke-Health",
    "sensor": "biometric"
  },
  "payload": {
    "type": "numeric",
    "data": 72,
    "unit": "bpm"
  }
}
```

## Ingestion Rules

1. All observations are append-only
2. No observation is ever deleted — only superseded by newer evidence
3. Every observation must have a source node
4. Raw data integrity is verified at ingestion

---
*Layer steward: Protocol Council*
*Version: 4.0*
