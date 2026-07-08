# ENTITY: agent-state-001
## Type: AgentState
## Canonical Name: PicoClaw Agent Context
## Status: migrated-from-legacy
## Source: phone_bootstrap/memory_agent_context.json

---

## DEFINITION

The operational state of the PicoClaw autonomous agent, including current mission, active skills, memory references, and decision history.

## ATTRIBUTES

| Attribute | Type | Value | Source |
|-----------|------|-------|--------|
| agent_id | string | "picoclaw-main" | config.reference.json |
| provider | string | "ollama" | config.reference.json |
| model | string | "llama3" | config.reference.json |
| max_tokens | integer | 2048 | config.reference.json |
| current_mission | string | [dynamic] | memory_agent_context.json |
| active_skills | array | [skill_list] | memory_skill_review_queue.json |
| last_execution | timestamp | [dynamic] | memory_implementations.json |
| health_status | string | "healthy" | memory_orchestrator_status.json |
| telegram_enabled | boolean | true | config.reference.json |
| gateway_host | string | "127.0.0.1" | config.reference.json |
| gateway_port | integer | 18790 | config.reference.json |

## RELATIONSHIPS

| Relationship | Target | Type |
|--------------|--------|------|
| runs_on | entity-device-termux | one-to-one |
| uses_model | entity-model-llama3 | one-to-one |
| communicates_via | entity-channel-telegram | one-to-many |
| stores_memory_in | entity-knowledge-base | one-to-one |
| governed_by | entity-system-config | one-to-one |
| executes_skills | entity-skill-queue | one-to-many |
| reports_to | entity-orchestrator | one-to-one |

## EVIDENCE

- Source file: `picoclaw-dev/archive/phone_bootstrap/memory_agent_context.json`
- Migrated at: 2026-07-08
- Migration agent: Kimi (Systems Architect)

## HISTORY

| Date | Event |
|------|-------|
| 2026-03-05 | Created in phone_bootstrap system |
| 2026-07-08 | Migrated to quillyos-nexus entity |

---

*Canonical entity in the QuillyOS Nexus*
