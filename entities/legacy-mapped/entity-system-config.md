# ENTITY: system-config-001
## Type: Configuration
## Canonical Name: PicoClaw System Configuration
## Status: migrated-from-legacy
## Source: phone_bootstrap/config.reference.json

---

## DEFINITION

The canonical configuration for the PicoClaw autonomous agent system, defining LLM providers, communication channels, model parameters, and gateway settings.

## ATTRIBUTES

| Attribute | Type | Value | Source |
|-----------|------|-------|--------|
| config_version | string | "1.0" | config.reference.json |
| default_provider | string | "ollama" | config.reference.json |
| default_model | string | "llama3" | config.reference.json |
| max_tokens | integer | 2048 | config.reference.json |
| telegram_enabled | boolean | true | config.reference.json |
| telegram_token | string | "REDACTED" | config.reference.json |
| telegram_allow_from | array | ["YOUR_USER_ID_HERE"] | config.reference.json |
| ollama_api_base | string | "http://localhost:11434/v1" | config.reference.json |
| ollama_api_key | string | "ollama" | config.reference.json |
| gateway_host | string | "127.0.0.1" | config.reference.json |
| gateway_port | integer | 18790 | config.reference.json |
| heartbeat_enabled | boolean | true | config.reference.json |

## RELATIONSHIPS

| Relationship | Target | Type |
|--------------|--------|------|
| configures | entity-agent-state | one-to-one |
| defines | entity-model-llama3 | one-to-one |
| enables | entity-channel-telegram | one-to-one |
| connects_to | entity-gateway-service | one-to-one |

## SECURITY NOTES

- `telegram_token` is REDACTED in Nexus. Actual token stored in device secure storage.
- `ollama_api_key` is "ollama" (no auth for local Ollama).
- Gateway port 18790 is internal only.

## EVIDENCE

- Source file: `picoclaw-dev/archive/phone_bootstrap/config.reference.json`
- Migrated at: 2026-07-08

---

*Canonical entity in the QuillyOS Nexus*
