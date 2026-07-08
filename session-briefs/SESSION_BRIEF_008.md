# SESSION BRIEF — Kimi — 2026-07-08
## Session ID: 2026-07-08-008
## Status: in-progress
## Agent: Kimi (Systems Architect & Integrator)
## Platform: Web (Kimi K2.6 Instant)
## Repository: `q-u-i-l-l-y/quillyos-nexus`

---

## WHAT WAS DONE (So Far)

- [x] **Pushed nexus-ingest.py v4.0** — Fixed `scan_device()` crash, stable classification engine
  - Commit: `67c7bc7c7370012ceefa66492361c354008fcfec`
- [x] **Pushed PicoClaw Agent v4.1** — DMSP Breathing Loop with 5-layer introspection
  - Commit: `2b234d75a876712ee7f147fde98549562a1559a3`
- [x] **Pushed workspace-bridge.py v1.0** — PicoClaw ↔ picostart Agent bridge
  - Commit: `36f3fcf30a77036fcba207d83a621c980034a80a`
- [x] **Verified Ollama + Qwen2.5:0.5B** running locally on Termux
- [x] **Verified picostart breathing loop** — DMSP introspection working
- [x] **Pulled latest from quillyos-foundation** — Got Master Vision Brief v4.0, DMSP v1.0, legacy mapping
- [x] **Tested workspace bridge** — `sync-state` works, `learn` needs reaction logs
- [x] **Identified Qwen 0.5B context overflow** — Prompt truncation at 4096 tokens, HTTP 500 timeouts

## CURRENT STATE

| Component | Status |
|-----------|--------|
| quillyos-nexus repo | Live on GitHub |
| nexus-ingest.py v4.0 | Pushed to main |
| PicoClaw Agent v4.1 | Pushed to main |
| Workspace Bridge v1.0 | Pushed to main, tested |
| Ollama (Qwen 0.5B) | Running but context-limited |
| PicoClaw (Go binary) | Configured, needs larger model |
| picostart (Python) | Working, breathing loop verified |
| Node identity | Registered (`node-1783531129-b8419160.json`) |
| `.bashrc` | Clean |
| Legacy mapping | Documented, not yet executed |
| Context Matrices | Empty (matrix-001, 002, 003 not yet populated) |

## KNOWN ISSUES

1. **PicoClaw context overflow** — AGENT.md + system prompt = ~4800 tokens, exceeds Qwen 0.5B 4096 limit
   - **Status:** Identified, needs model upgrade
   - **Fix:** Switch to Qwen 3.5 (larger context window) or Qwen 1.8B/4B
2. **PicoClaw timeout** — First inference takes 60-80s on CPU, causing HTTP 500
   - **Status:** Partially mitigated by prompt cache (second run faster)
   - **Fix:** Use `--no-warmup` or enable GPU if available
3. **mcp_bridge skill** — Invalid name (underscore), needs rename to `mcp-bridge`
4. **No reaction logs** — `workspace-bridge.py learn` reports no logs to learn from
   - **Fix:** Need to run breathing loop after commits to generate REACTION_*.md files

## NEXT ACTION: SWITCH TO QWEN 3.5

The user requested switching from Qwen 2.5 0.5B to **Qwen 3.5** for larger context window and better performance.

### Qwen 3.5 Models Available

| Model | Size | Context | VRAM/RAM | Best For |
|-------|------|---------|----------|----------|
| `qwen3:0.6b` | 0.6B | 32K | ~400MB | Ultra-light edge |
| `qwen3:1.7b` | 1.7B | 32K | ~1.1GB | Balanced edge |
| `qwen3:4b` | 4B | 32K | ~2.5GB | Better reasoning |
| `qwen3:8b` | 8B | 32K | ~5GB | Desktop-class |
| `qwen3:30b` | 30B | 32K | ~18GB | Server-class |

### Recommended for Termux (3.5GB RAM)

**`qwen3:1.7b`** — 1.7B params, 32K context, ~1.1GB RAM usage
- 3× larger context than 0.5B (32K vs 4K effective)
- Better reasoning for revenue engine tasks
- Fits comfortably in 3.5GB system with swap

### Migration Commands

```bash
# Pull Qwen 3.5 1.7B
ollama pull qwen3:1.7b

# Update PicoClaw config
sed -i 's/qwen2.5:0.5b/qwen3:1.7b/g' ~/.picoclaw/config.json

# Restart Ollama
pkill ollama
ollama serve &

# Test with new model
picoclaw agent -m "What is my current mission?"
```

## PRIORITY QUEUE (Session 008)

1. **Switch to Qwen 3.5** — `ollama pull qwen3:1.7b`, update config, test inference
2. **Test workspace bridge** — Run `introspect`, `sync-state`, `learn` with new model
3. **Fix mcp_bridge skill name** — Rename to `mcp-bridge`
4. **Generate reaction logs** — Run breathing loop after next commit to create REACTION_*.md
5. **Map phone_bootstrap to entities** — Execute LAYER_MAPPING.md
6. **Populate Context Matrices** — Fill matrix-001, 002, 003 with live project data
7. **Test clone-to-node installer** — Verify `install.sh` works on fresh Termux

## CRITICAL CONTEXT FOR NEXT KIMI

- **Qwen 3.5 switch is pending** — User explicitly requested this upgrade
- **nexus-ingest.py v4.0** is canonical on `main` — pull before any scan
- **Workspace Bridge** connects PicoClaw memory to Nexus entities
- **Agent tandem mode** requires: ingestor JSON → agent reads → presents choices → executes follow-up
- **Legacy system** mapping is documented but not executed — `entities/` needs population
- **Context Matrices** (matrix-001, 002, 003) should live in `contexts/` and map to DMSP v1.0 layers
- **All 5 repos exist**: `quillyos-foundation`, `quillyos-nexus`, `picoclaw-dev` (private), `picoclaw-skills`, `quillyos-knowledge-base` (private)

## IMMEDIATE ACTION FOR USER

```bash
# Switch to Qwen 3.5 1.7B
ollama pull qwen3:1.7b

# Update PicoClaw config
sed -i 's/qwen2.5:0.5b/qwen3:1.7b/g' ~/.picoclaw/config.json

# Restart Ollama
pkill ollama
ollama serve &

# Test with new model
picoclaw agent -m "What is my current mission?"

# Paste output for next Kimi session
```

---

*Generated by Kimi at 2026-07-08T15:58:00Z*
*Repository: https://github.com/q-u-i-l-l-y/quillyos-nexus*
