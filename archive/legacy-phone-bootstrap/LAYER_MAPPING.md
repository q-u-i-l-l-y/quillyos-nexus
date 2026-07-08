# LEGACY SYSTEM → NEXUS LAYER MAPPING
## phone_bootstrap / quillyos-nexus Integration Guide
## Version: 1.0

---

## COMPLETE FILE INVENTORY

### LAYER 0: OBSERVATION (Raw Data Capture)

| File | Purpose | Nexus Destination |
|------|---------|-------------------|
| `crawler.py` | Web scraping engine | `nexus/layer0/observations/crawler-engine.md` |
| `crawler_v2.py` | Enhanced crawler | `nexus/layer0/observations/crawler-v2-engine.md` |
| `revenue_tracker.json` | Financial observation store | `nexus/layer0/raw/revenue-observations.json` |
| `memory_wallet.json` | Wallet state observations | `nexus/layer0/raw/wallet-observations.json` |
| `memory_discoveries.json` | Novel finding observations | `nexus/layer0/raw/discovery-observations.json` |

**Entity Type:** `ObservationStream`
**Attributes:** source, timestamp, raw_data, checksum

---

### LAYER 1: EVIDENCE (Pattern Extraction)

| File | Purpose | Nexus Destination |
|------|---------|-------------------|
| `analyzer.py` | General pattern analysis | `nexus/layer1/evidence/analyzer-engine.md` |
| `deal_analyzer_skill.py` | Deal pattern extraction | `nexus/layer1/evidence/deal-analysis-skill.md` |
| `lead_discovery_skill.py` | Lead pattern extraction | `nexus/layer1/evidence/lead-discovery-skill.md` |
| `quality_gate_skill.py` | Evidence quality filter | `nexus/layer1/evidence/quality-gate-skill.md` |
| `memory_deal_analysis.json` | Extracted deal evidence | `nexus/layer1/patterns/deal-evidence.json` |
| `memory_discussion_analysis.json` | Conversation evidence | `nexus/layer1/patterns/discussion-evidence.json` |
| `error_recovery.json` | Anomaly evidence | `nexus/layer1/anomalies/error-patterns.json` |

**Entity Type:** `EvidenceRecord`
**Attributes:** pattern_type, confidence, source_observation, extracted_features

---

### LAYER 2: CONTEXT (Structured Understanding)

| File | Purpose | Nexus Destination |
|------|---------|-------------------|
| `config.reference.json` | Canonical configuration | `nexus/layer2/entities/entity-system-config.md` |
| `memory_agent_context.json` | Agent state | `nexus/layer2/entities/entity-agent-state.md` |
| `memory_bot_state.json` | Bot operational state | `nexus/layer2/entities/entity-bot-state.md` |
| `memory_orchestration.json` | Orchestration plan | `nexus/layer2/entities/entity-orchestration.md` |
| `memory_orchestrator_status.json` | Orchestrator health | `nexus/layer2/entities/entity-orchestrator-health.md` |
| `memory_knowledge_base.json` | Domain knowledge | `nexus/layer2/entities/entity-knowledge-base.md` |
| `memory_best_practices.json` | Operational wisdom | `nexus/layer2/entities/entity-best-practices.md` |
| `memory_implementation_plan.json` | Execution plan | `nexus/layer2/entities/entity-implementation-plan.md` |
| `memory_implementations.json` | History of execution | `nexus/layer2/entities/entity-implementation-history.md` |
| `memory_deployment_status.json` | Deployment health | `nexus/layer2/entities/entity-deployment-status.md` |
| `memory_skill_review_queue.json` | Skill backlog | `nexus/layer2/entities/entity-skill-queue.md` |

**Entity Type:** Various (see individual entity definitions)
**Common Attributes:** entity_id, type, version, created_at, updated_at, source_file

---

### LAYER 3: TRANSLATION (Agent Format Conversion)

| File | Purpose | Nexus Destination |
|------|---------|-------------------|
| `orchestrator.py` | Agent coordination | `nexus/layer3/picoclaw/orchestrator-translator.md` |
| `telegram_bot.py` | Telegram interface | `nexus/layer3/picoclaw/telegram-channel.md` |
| `telegram_bot_handler.py` | Message handling | `nexus/layer3/picoclaw/telegram-handler.md` |
| `picoclaw_telegram_bot.py` | PicoClaw bridge | `nexus/layer3/picoclaw/picoclaw-telegram-bridge.md` |
| `picoclaw_telegram_handler.py` | PicoClaw handler | `nexus/layer3/picoclaw/picoclaw-message-handler.md` |
| `telegram_commands.py` | Command mapping | `nexus/layer3/picoclaw/telegram-command-map.md` |
| `skill_generator.py` | Skill manifest gen | `nexus/layer3/picoclaw/skill-generator.md` |
| `update_config.py` | Config updater | `nexus/layer3/picoclaw/config-updater.md` |
| `fix_model.py` | Model repair | `nexus/layer3/picoclaw/model-repair-translator.md` |
| `notifier.py` | Alert dispatcher | `nexus/layer3/n8n/notification-workflow.md` |

**Entity Type:** `TranslationLayer`
**Attributes:** source_format, target_format, agent_target, conversion_rules

---

### LAYER 4: CONSENSUS (Decision & Execution)

| File | Purpose | Nexus Destination |
|------|---------|-------------------|
| `deal_validator.json` | Deal approval logic | `nexus/layer4/decisions/deal-validation-rules.md` |
| `margin_optimizer.json` | Execution optimization | `nexus/layer4/decisions/margin-optimization-rules.md` |
| `rollback_manager.json` | Error recovery | `nexus/layer4/decisions/rollback-policies.md` |
| `skill_improver.json` | Skill evolution | `nexus/layer4/decisions/skill-improvement-rules.md` |
| `repository.json` | Code governance | `nexus/layer4/decisions/repository-governance.md` |
| `autonomous.py` | Autonomous execution | `nexus/layer4/executions/autonomous-engine.md` |
| `bot_improved.py` | Enhanced execution | `nexus/layer4/executions/improved-bot-engine.md` |
| `picoclaw_self_bootstrap.py` | Self-healing | `nexus/layer4/executions/self-bootstrap-engine.md` |

**Entity Type:** `ConsensusRecord`
**Attributes:** proposal, agents_involved, consensus_type, confidence, execution_result

---

## RELATIONSHIP MAP

```
Layer 0 (crawler.py) → Layer 1 (analyzer.py) → Layer 2 (memory_knowledge_base.json)
     ↓                        ↓                        ↓
revenue_tracker.json    deal_analyzer_skill.py   config.reference.json
     ↓                        ↓                        ↓
Layer 3 (orchestrator.py) → Layer 4 (deal_validator.json) → Superimposition
```

**Key Relationships:**
- `crawler.py` → `analyzer.py`: Raw crawl → Pattern extraction
- `analyzer.py` → `memory_knowledge_base.json`: Evidence → Structured knowledge
- `memory_knowledge_base.json` → `orchestrator.py`: Knowledge → Agent coordination
- `orchestrator.py` → `deal_validator.json`: Coordination → Consensus
- `deal_validator.json` → `margin_optimizer.json`: Approval → Optimization
- `margin_optimizer.json` → `rollback_manager.json`: Execution → Recovery

---

## MIGRATION CHECKLIST

### Phase 1: Archive (Preserve)
- [ ] Copy all 24 Python files to `nexus/archive/legacy-phone_bootstrap/python/`
- [ ] Copy all 25 JSON files to `nexus/archive/legacy-phone_bootstrap/json/`
- [ ] Copy `config.reference.json` to `nexus/archive/legacy-phone_bootstrap/config/`
- [ ] Document origin: `nexus/archive/legacy-phone_bootstrap/README.md`

### Phase 2: Extract (Entity Creation)
- [ ] Create entity definitions for all 11 Layer 2 memory files
- [ ] Create entity definitions for all 5 Layer 4 decision files
- [ ] Map relationships between entities
- [ ] Validate entity completeness

### Phase 3: Convert (Translation)
- [ ] Convert Python scripts to Markdown skill definitions
- [ ] Convert JSON configs to Markdown entity definitions
- [ ] Create n8n workflow equivalents for Layer 3/4 scripts
- [ ] Test translation accuracy

### Phase 4: Generate (Superimposition)
- [ ] Run first superimposition across all layers
- [ ] Identify emergent patterns
- [ ] Generate trend reports
- [ ] Feed insights back into Layer 2 context

---

*Migration guide for phone_bootstrap → quillyos-nexus*
