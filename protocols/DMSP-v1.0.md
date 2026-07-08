# DATA MATRICES SUPERIMPOSITION PROTOCOL (DMSP)
## Version: 1.0
## Status: Draft
## Part of: QuillyOS Nexus Protocol

---

## CORE PRINCIPLE

> Just as superimposing data matrices reveals trends that arise from natural events, so too should our protocol be structured in layers that, when overlaid, reveal emergent patterns in collective intelligence.

## THE LAYER MODEL

### Layer 0: Raw Observation Matrix
**Purpose:** Capture reality as it occurs, without interpretation.

**Sources:**
- Sensor telemetry (ENDS device: HR, SpO2, temp, respiration)
- Chat logs (Telegram, Discord, CLI)
- Market data (arbitrage, trading, deal flow)
- Web crawls (crawler.py, crawler_v2.py)
- Device state (battery, network, compute load)
- Human input (voice, text, gesture)

**Format:** Unstructured or semi-structured raw data
**Storage:** `nexus/layer0/observations/YYYY-MM-DD/`
**Retention:** Ephemeral (24h) unless flagged for extraction

**Legacy Mapping:**
| Legacy File | Layer 0 Role |
|-------------|--------------|
| `crawler.py` | Web observation engine |
| `crawler_v2.py` | Enhanced observation engine |
| `revenue_tracker.json` | Market observation store |
| `memory_wallet.json` | Financial observation store |
| `memory_discoveries.json` | Novel observation store |

---

### Layer 1: Evidence Extraction Matrix
**Purpose:** Extract patterns, anomalies, and signals from raw observations.

**Processes:**
- Pattern recognition (regex, ML, heuristic)
- Anomaly detection (statistical deviation, threshold breach)
- Filtering (noise reduction, relevance scoring)
- Classification (tagging, categorization)
- Deduplication (merge similar observations)

**Format:** Structured evidence records with confidence scores
**Storage:** `nexus/layer1/evidence/YYYY-MM-DD/`
**Retention:** Medium-term (30 days) or until incorporated into context

**Legacy Mapping:**
| Legacy File | Layer 1 Role |
|-------------|--------------|
| `analyzer.py` | Pattern extraction engine |
| `deal_analyzer_skill.py` | Deal evidence extraction |
| `lead_discovery_skill.py` | Lead evidence extraction |
| `quality_gate_skill.py` | Evidence quality filtering |
| `memory_deal_analysis.json` | Extracted deal evidence |
| `memory_discussion_analysis.json` | Extracted conversation evidence |
| `error_recovery.json` | Anomaly evidence store |

---

### Layer 2: Context Matrix
**Purpose:** Structure understanding into canonical entities, relationships, and states.

**Components:**
- Entity definitions (canonical types, attributes, relationships)
- Context matrices (mission-specific knowledge packages)
- Knowledge graph (entity-relationship map)
- State snapshots (system state at a point in time)

**Format:** Markdown entities + JSON relationship maps
**Storage:** `nexus/contexts/`, `nexus/entities/`, `nexus/relationships/`
**Retention:** Permanent (version-controlled)

**Legacy Mapping:**
| Legacy File | Layer 2 Role |
|-------------|--------------|
| `config.reference.json` | Canonical configuration entity |
| `memory_agent_context.json` | Agent state entity |
| `memory_bot_state.json` | Bot state entity |
| `memory_orchestration.json` | Orchestration state entity |
| `memory_orchestrator_status.json` | Orchestrator status entity |
| `memory_knowledge_base.json` | Knowledge base entity |
| `memory_best_practices.json` | Best practices entity |
| `memory_implementation_plan.json` | Plan entity |
| `memory_implementations.json` | Implementation history entity |
| `memory_deployment_status.json` | Deployment status entity |
| `memory_skill_review_queue.json` | Skill queue entity |

---

### Layer 3: Agent Translation Matrix
**Purpose:** Convert context into agent-specific formats for reasoning.

**Processes:**
- Format conversion (Markdown → JSON → Python dict → etc.)
- Context window optimization (compress for token limits)
- Agent package assembly (mission + evidence + constraints)
- Skill manifest generation (for PicoClaw skill loading)

**Format:** Agent-specific packages
**Storage:** `nexus/translations/`
**Retention:** Ephemeral (regenerated per session)

**Legacy Mapping:**
| Legacy File | Layer 3 Role |
|-------------|--------------|
| `orchestrator.py` | Agent coordination translator |
| `telegram_bot.py` | Telegram channel translator |
| `telegram_bot_handler.py` | Telegram message translator |
| `picoclaw_telegram_bot.py` | PicoClaw-Telegram bridge |
| `picoclaw_telegram_handler.py` | PicoClaw message handler |
| `telegram_commands.py` | Command translation map |
| `skill_generator.py` | Skill manifest translator |
| `update_config.py` | Config update translator |
| `fix_model.py` | Model repair translator |

---

### Layer 4: Consensus & Execution Matrix
**Purpose:** Aggregate agent outputs, reach consensus, execute decisions.

**Processes:**
- Proposal aggregation (collect agent recommendations)
- Consensus detection (find agreement across agents)
- Conflict resolution (vote, escalate, or defer)
- Execution routing (dispatch to n8n, PicoClaw, or human)
- Feedback loop (record outcomes for learning)

**Format:** Decision records + execution logs
**Storage:** `nexus/consensus/`
**Retention:** Permanent (governance record)

**Legacy Mapping:**
| Legacy File | Layer 4 Role |
|-------------|--------------|
| `deal_validator.json` | Deal consensus validator |
| `margin_optimizer.json` | Execution optimizer |
| `rollback_manager.json` | Execution rollback controller |
| `skill_improver.json` | Skill improvement consensus |
| `repository.json` | Code consensus tracker |
| `autonomous.py` | Autonomous execution engine |
| `bot_improved.py` | Improved execution logic |
| `picoclaw_self_bootstrap.py` | Self-healing execution |

---

## SUPERIMPOSITION OPERATION

### Definition
Superimposition is the act of overlaying all five layers to reveal emergent structure that no single layer contains.

### Mathematical Analogy
```
Let M₀ = Observation Matrix (Layer 0)
Let M₁ = Evidence Matrix (Layer 1)  
Let M₂ = Context Matrix (Layer 2)
Let M₃ = Translation Matrix (Layer 3)
Let M₄ = Consensus Matrix (Layer 4)

Superimposition S = M₀ ⊗ M₁ ⊗ M₂ ⊗ M₃ ⊗ M₄

Where ⊗ represents the superimposition operator:
- Not simple addition (not M₀ + M₁)
- Not simple multiplication (not M₀ × M₁)
- But intersection of patterns across layers

Emergent Pattern P = f(S) where f is the pattern recognition function
```

### Practical Example

**Scenario:** A deal appears in the revenue tracker.

**Layer 0:** `revenue_tracker.json` logs a new deal opportunity.
**Layer 1:** `deal_analyzer_skill.py` extracts: "Deal margin = 23%, risk = medium"
**Layer 2:** `memory_deal_analysis.json` contextualizes: "Similar deals have 18% avg margin"
**Layer 3:** `orchestrator.py` translates to Kimi package: "Evaluate deal X against historical baseline"
**Layer 4:** `deal_validator.json` reaches consensus: "Approve with 85% confidence"

**Superimposition:** The emergent pattern is not just "deal approved" but "this deal type represents a new market segment with above-average margins, suggesting a strategic pivot opportunity."

---

## IMPLEMENTATION

### File Structure
```
nexus/
├── layer0/
│   ├── observations/
│   ├── sensors/
│   └── raw/
├── layer1/
│   ├── evidence/
│   ├── patterns/
│   └── anomalies/
├── layer2/
│   ├── contexts/          (Context matrices)
│   ├── entities/          (Canonical definitions)
│   └── relationships/     (Entity maps)
├── layer3/
│   ├── kimi/              (Kimi context packages)
│   ├── picoclaw/          (PicoClaw skill manifests)
│   ├── n8n/               (n8n workflow configs)
│   └── human/             (Human-readable summaries)
├── layer4/
│   ├── decisions/         (Consensus records)
│   ├── executions/        (Execution logs)
│   └── feedback/          (Outcome feedback)
└── superimposition/
    ├── trends/             (Emergent trend reports)
    ├── alerts/             (Anomaly alerts)
    └── insights/           (Strategic insights)
```

### Pipeline
```
Observation → Evidence → Context → Translation → Consensus → Superimposition
    ↓            ↓          ↓           ↓            ↓              ↓
  Layer 0     Layer 1    Layer 2    Layer 3     Layer 4    Emergent Output
```

---

## LEGACY SYSTEM INTEGRATION

### Migration Path

```
phone_bootstrap/
├── Layer 0: Crawlers, trackers, wallets, discoveries
├── Layer 1: Analyzers, deal skills, lead skills, quality gates
├── Layer 2: Memory files, configs, knowledge bases, plans
├── Layer 3: Orchestrator, bots, handlers, generators, fixers
└── Layer 4: Validators, optimizers, rollback, improvers, autonomous
```

Each legacy component maps to exactly one layer. During migration:
1. **Preserve** the original in `nexus/archive/legacy-phone_bootstrap/`
2. **Extract** entities into `nexus/layer2/entities/`
3. **Convert** scripts into `nexus/layer3/` translations or n8n workflows
4. **Generate** superimposition reports in `nexus/superimposition/`

---

## VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-07-08 | Initial draft, legacy mapping complete |

---

*Part of the QuillyOS Nexus Protocol*
*Build for decades. Not versions.*
