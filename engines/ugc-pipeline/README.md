# QuillyOS UGC Pipeline v0.1
## engines/ugc-pipeline/

**Status:** Operational (dry-run) | **Commit:** dc5a111

---

## Architecture

The UGC Pipeline is a **Tier 2 Revenue Engine** within the QuillyOS ecosystem.
It sits alongside the Agent Orchestrator and consumes the same API vault.

```
┌─────────────────────────────────────────────────────────────┐
│                    QUILLYOS NEXUS                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌───────────────┐  │
│  │  Agent Orche- │  │  UGC Pipeline   │  │  Key Vault    │  │
│  │  strator v3.1  │  │  (this dir)     │  │  ~/.quillyos/ │  │
│  │                 │  │                 │  │  keys/        │  │
│  │  • Health checks│  │  • discover.py  │  │               │  │
│  │  • API metrics  │  │  • generate.py  │  │  40 APIs      │  │
│  │  • DB logging   │  │  • distribute.py│  │  3 working    │  │
│  └─────────────────┘  │  • pipeline.py  │  │  6 pending    │  │
│         ▲              └─────────────────┘  └───────────────┘  │
│         │                      │                               │
│         └────── shared ────────┘                               │
│              load_key() helper                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Module Map

| File | Role | Depends On | Free Tier Limits |
|------|------|------------|------------------|
| `discover.py` | Content discovery | Tavily (key), HN (keyless), Wikipedia (keyless) | Tavily: 1,000 calls/mo |
| `generate.py` | LLM post generation | OpenRouter (key) or Groq (pending) | OpenRouter: pay-as-you-go; Groq: 14.4K tok/min |
| `distribute.py` | Telegram posting | Telegram Bot API (key) | 30 msgs/sec |
| `pipeline.py` | Orchestrator | All three modules | N/A |

---

## How It Fits the Master Vision

> **QuillyOS is a model-agnostic shared understanding repository.**

The UGC Pipeline extends this from *passive* knowledge storage to *active*
knowledge curation:

1. **Discovery** harvests signal from the mesh (Tavily, HN, Wikipedia)
2. **Generation** distills signal into wisdom via LLM (OpenRouter/Groq)
3. **Distribution** broadcasts wisdom back to the mesh (Telegram)

Each post is a **knowledge artifact** that can be traced back to its source
APIs, logged in `agent_state.db`, and refined over time.

---

## Usage

### Dry-run (default)
```bash
cd ~/quillyos-nexus/engines/ugc-pipeline
python pipeline.py "artificial intelligence"
```

### Live Telegram post
1. Set your chat ID in `distribute.py`:
   ```bash
   python3 -c "from pathlib import Path; p=Path('distribute.py'); p.write_text(p.read_text().replace('@your_channel_name', '@your_channel'))"
   ```
2. Uncomment the post line in `pipeline.py`:
   ```bash
   python3 -c "from pathlib import Path; p=Path('pipeline.py'); p.write_text(p.read_text().replace('# await post_to_telegram(post)', 'await post_to_telegram(post)'))"
   ```
3. Run again.

### Cron automation
```bash
crontab -e
# Add:
0 */6 * * * cd ~/quillyos-nexus/engines/ugc-pipeline && python pipeline.py >> pipeline.log 2>&1
```

---

## Next Evolution

- [ ] **Groq integration** — swap provider for faster/cheaper generation
- [ ] **NewsData integration** — replace Tavily as primary news source
- [ ] **Amazon Associates** — append affiliate links to generated posts
- [ ] **A/B testing** — track engagement per post format in `agent_state.db`
- [ ] **PicoClaw agent mode** — run lightweight pipeline on ENDS device

---

## Constraints

- Termux-safe: all file ops use `pathlib`, no heredocs
- Free-tier only: all APIs use gratis limits
- Ghost operation: no paid credits, no background billing
- Git-safe: `.gitignore` excludes `__pycache__`, logs, and `.env`
