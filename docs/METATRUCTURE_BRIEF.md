# QuillyOS Ecosystem Metastructure Brief
## For Cross-Agent Collaboration | Generated: 2026-07-11

---

## EXECUTIVE SUMMARY

This document maps the complete QuillyOS repository ecosystem as a **global workspace** — a model-agnostic shared understanding repository where each repo is a specialized node in a mesh. The goal is to maximize cross-repo synergy, prevent duplicate work, and ensure every agent instance understands the whole before modifying any part.

**Author:** q-u-i-l-l-y  
**Canonical Repos:** quillyos-nexus, quillyos-foundation, picoclaw-skills  
**Device:** ENDS (modular nexus)  
**Agent Runtime:** Kimi K2.6 (cloud) + PicoClaw (local, ~800MB RAM)

---

## REPOSITORY TOPOLOGY

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         QUILLYOS ECOSYSTEM                               │
│                                                                          │
│  ┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────┐  │
│  │  quillyos-nexus     │◄──►│  quillyos-foundation │◄──►│picoclaw-    │  │
│  │  (Revenue Engine)   │    │  (Canonical Truth)   │    │skills       │  │
│  │                     │    │                     │    │(Onboarding) │  │
│  │  • engines/         │    │  • vision/          │    │             │  │
│  │    - agent-orchestr │    │    - MASTER_VISION   │    │  • Tier 4   │  │
│  │    - ugc-pipeline   │    │    - nexus_matrix    │    │    public   │  │
│  │    - frontend/      │    │  • entity-*.md       │    │    repo     │  │
│  │  • keys/ (gitignore)│    │  • data-matrices/    │    │  • phone_   │  │
│  │  • agent_state.db   │    │                     │    │    bootstrap│  │
│  │                     │    │  Immutable layer:    │    │  • 24 Python│  │
│  │  ACTIVE DEVELOPMENT │    │  - Project identity  │    │  • 25 JSON  │  │
│  │                     │    │  - Entity maps       │    │             │  │
│  └─────────────────────┘    └─────────────────────┘    └─────────────┘  │
│           ▲                          ▲                          ▲       │
│           │                          │                          │       │
│           └──────────┬───────────────┘                          │       │
│                      SHARED                                      │       │
│                      VAULT                                       │       │
│              ~/.quillyos/keys/                                 │       │
│              ~/.quillyos/brief/                                  │       │
│                      ▲                                           │       │
│                      │                                           │       │
│              ┌───────┴───────┐                                   │       │
│              │   pull-brief    │◄──────────────────────────────────┘       │
│              │   v4.0          │                                          │
│              │   (unified)     │                                          │
│              └───────────────┘                                          │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │  MESH PRINCIPLE: Clone repo = become mesh node                      │ │
│  │  nexus_matrix.json is the canonical entity map                      │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## PER-REPOSITORY CONTRACT

### quillyos-nexus (Active Development Layer)

**Role:** Where code lives, runs, and evolves. The "engine room."

**Directory Map:**
```
engines/
├── agent-orchestrator/     # v3.1 — API health, vault management, DB logging
│   ├── agent_orchestrator.py
│   └── migrate_v3.py
├── ugc-pipeline/             # v0.1 — Content discovery → generation → distribution
│   ├── discover.py           # Tavily + HN + Wikipedia
│   ├── generate.py           # OpenRouter/Groq LLM post generation
│   ├── distribute.py         # Telegram Bot API posting
│   ├── pipeline.py           # Unified orchestrator (dry-run default)
│   ├── __init__.py
│   ├── .gitignore
│   └── README.md
└── frontend/                 # v0.1 — Human interaction layer
    ├── telegram_bot.py       # Primary: mobile-native bot commands
    ├── cli_dashboard.py      # Secondary: terminal overview
    └── html_report.py        # Tertiary: per-run static reports

keys/                         # GITIGNORED — never committed
├── *.key (40 API keys)
└── amazon_associate.key      # PENDING — revenue unlock

agent_state.db                # GITIGNORED — operational telemetry
```

**Agent Rules for This Repo:**
- ALL code is Termux-safe (Python one-liners, no heredocs)
- ALL APIs are free-tier (ghost operation)
- NEVER commit keys/ or *.db
- Git commit after every milestone
- Async/await for all I/O (httpx)

**Current Velocity:**
- 16/40 APIs healthy
- 3 working keys (OpenRouter, Tavily, Telegram)
- Pipeline: dry-run operational
- Bot: live and responding (@V1_pico_partner_bot)
- Admin: Notquilly (ID: 5602955210)

---

### quillyos-foundation (Canonical Truth Layer)

**Role:** Immutable project identity. The "constitution." This repo should never contain operational code — only documents that define what QuillyOS is, why it exists, and how entities relate.

**Expected Structure (to be verified/created):**
```
vision/
├── MASTER_VISION_BRIEF.md    # v4.0 — Immutable project identity
└── REVENUE_STRATEGY.md        # Monetization roadmap

data-matrices/
├── nexus_matrix.json          # Canonical entity map (all repos, all nodes)
├── entity-agent-state.md      # Agent runtime state schema
└── entity-system-config.md    # System configuration schema

onboarding/
└── MIGRATION_GUIDE.md         # phone_bootstrap → nexus migration path
```

**Agent Rules for This Repo:**
- APPEND-ONLY — never overwrite, only add dated versions
- Every change is a pull request, never direct push to main
- Documents are Markdown with YAML frontmatter for machine parsing
- Cross-references use permanent anchors (##section-name) not line numbers

**Current Gap:** CANONICAL_BRIEF.md exists in `~/.quillyos/brief/` but not in the foundation repo. This is a drift risk.

---

### picoclaw-skills (Onboarding / Tier 4 Public Layer)

**Role:** Public-facing onboarding repo. The "front door." Anyone can clone this and understand QuillyOS without accessing private keys or revenue systems.

**Expected Structure:**
```
scripts/
├── pull-brief-fallback.py     # Standalone brief reader (no deps)
├── phone_bootstrap/          # Legacy: 24 Python + 25 JSON
│   ├── bootstrap.py
│   └── config/
└── setup_ends.sh             # ENDS device initialization

docs/
├── GETTING_STARTED.md
├── ARCHITECTURE.md
└── CONTRIBUTING.md

skills/
└── (public skill modules for mesh nodes)
```

**Agent Rules for This Repo:**
- Must run on ENDS hardware (~800MB RAM, no GPU)
- Uses Qwen 2.5 0.5B via Ollama on localhost:11434
- TinyLlama is deprecated (lacks tool support)
- All scripts must be copy-paste safe (no heredocs)

**Current Gap:** Legacy phone_bootstrap scripts exist but migration to nexus entities is incomplete.

---

## CROSS-REPO DEPENDENCY MAP

| If you modify... | You must also update... | Why |
|------------------|------------------------|-----|
| `nexus/engines/ugc-pipeline/*.py` | `foundation/vision/REVENUE_STRATEGY.md` | Pipeline changes affect monetization |
| `nexus/engines/frontend/telegram_bot.py` | `foundation/data-matrices/entity-agent-state.md` | Bot commands are agent runtime surface |
| `nexus/agent_state.db` schema | `foundation/data-matrices/entity-system-config.md` | DB schema is system config |
| `nexus/keys/*.key` (add/remove) | `nexus/engines/agent-orchestrator/` health checks | Vault changes affect orchestrator |
| `foundation/MASTER_VISION_BRIEF.md` | `picoclaw-skills/docs/ARCHITECTURE.md` | Public docs must reflect canonical vision |
| `pull-brief` (any version) | ALL repos' `.bashrc` / setup scripts | Brief is the universal interface |

---

## THE `pull-brief` AS NERVOUS SYSTEM

`pull-brief` is not just a script — it's the **shared cognitive layer** across all repos and all agent instances.

**Version Evolution:**
- v1.x: Static file reader (legacy)
- v2.x: Bash script with subcommands
- v3.2: Unified (legacy + live DB queries)
- v4.0: Versioned, canonical + session + live data

**Deployment:**
- Primary: `~/.quillyos/pull-brief`
- Fallbacks: `~/.picoclaw/bin/pull-brief`, `~/quillyos-foundation/scripts/`
- All versions must be backward-compatible with `legacy` subcommand

**For Agents:**
- ALWAYS run `pull-brief` first to understand current state
- NEVER assume the previous agent left things clean — verify
- Append to SESSION_LOG.md after every session (never overwrite)

---

## REVENUE ARCHITECTURE (Current + Future)

```
┌─────────────────────────────────────────────────────────────┐
│  TIER 1: CONTENT PRODUCTION (Operational)                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐    │
│  │  discover   │→│  generate   │→│  distribute     │    │
│  │  (Tavily)   │  │ (OpenRouter)│  │ (Telegram Bot)  │    │
│  └─────────────┘  └─────────────┘  └─────────────────┘    │
│         ↑                                          ↓        │
│         └───────────── pipeline.py ─────────────────┘        │
│                                                             │
│  TIER 2: MONETIZATION (Pending)                            │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │ Amazon Associates│  │ Sponsored Posts │                  │
│  │ (affiliate links)│  │ (paid features) │                  │
│  └─────────────────┘  └─────────────────┘                   │
│                                                             │
│  TIER 3: SCALE (Future)                                    │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │ Premium API Tier │  │ PicoClaw Bundles│                  │
│  │ (subscription)   │  │ (hardware + sw) │                  │
│  └─────────────────┘  └─────────────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

**Current Blockers to Revenue:**
1. Amazon Associates ID missing → needs Substack + application
2. Live posting disabled → needs Telegram chat_id + uncomment
3. Groq/NewsData pending → nice-to-have, not revenue-critical

---

## AGENT COLLABORATION PROTOCOL

When a new agent instance starts:

1. **Read** `pull-brief` (default) — understand current operational state
2. **Read** `pull-brief canonical` — understand immutable identity
3. **Read** `pull-brief log` — understand full history
4. **Verify** repo structure matches this brief — detect drift
5. **Execute** task — modify only the repo/layer appropriate for the task
6. **Commit** with tag `[AGENT]` — push to GitHub
7. **Append** session results to SESSION_LOG.md
8. **Update** `pull-brief` if structural changes occurred

**Cross-Repo Changes:**
- If modifying nexus operational code → update foundation docs
- If modifying foundation canonical docs → update picoclaw public docs
- If modifying pull-brief → update all repo fallback locations

---

## KNOWN DRIFT & TECHNICAL DEBT

| Issue | Location | Severity | Fix |
|-------|----------|----------|-----|
| CANONICAL_BRIEF.md empty | `~/.quillyos/brief/` | HIGH | Write immutable identity |
| phone_bootstrap legacy | `picoclaw-skills/` | MEDIUM | Complete migration to nexus |
| nexus_matrix.json missing | `quillyos-foundation/` | HIGH | Create canonical entity map |
| Groq key pending | Vault | LOW | Signup at console.groq.com |
| NewsData key pending | Vault | LOW | Signup at newsdata.io |
| giphy.key working but unused | Vault | LOW | Integrate into pipeline for image posts |
| github.key present but untested | Vault | LOW | Verify GitHub API access |

---

## FOR GPT COLLABORATION

This brief is designed for **cross-model comprehension**. Any GPT instance (Kimi, Claude, GPT-4, local Qwen) should be able to:

1. Parse this Markdown structure
2. Understand the repo topology without accessing the repos
3. Know which layer to modify for which task
4. Understand the `pull-brief` contract
5. Follow the agent collaboration protocol

**Key phrases for GPT context injection:**
- "QuillyOS is a model-agnostic shared understanding repository"
- "Clone repo = become mesh node"
- "ENDS device is modular nexus"
- "picoclaw-skills is Tier 4 public onboarding repo"
- "Master Vision Brief v4.0 is canonical at vision/MASTER_VISION_BRIEF.md"
- "Termux breaks heredocs — use Python one-liners"
- "PicoClaw runs on ~800MB RAM — Qwen 2.5 0.5B for agent mode"

---

## NEXT ACTIONS FOR ECOSYSTEM HARDENING

1. **Sync CANONICAL_BRIEF.md** from `~/.quillyos/brief/` to `quillyos-foundation/vision/`
2. **Create nexus_matrix.json** mapping all repos, files, and dependencies
3. **Migrate phone_bootstrap** scripts to nexus entity format
4. **Add GitHub Actions** (if available) for automated health checks on push
5. **Document the frontend API** (Telegram bot commands) in `foundation/data-matrices/`
6. **Create CHANGELOG.md** in nexus root for operational changes

---

*This brief is append-only. Add dated sections at the top for new insights.*
*For questions: run `pull-brief` or read `SESSION_LOG.md`.*
