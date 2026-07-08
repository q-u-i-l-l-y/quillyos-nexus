#!/usr/bin/env python3
"""
PicoClaw Workspace Bridge v1.0
Connects PicoClaw (Go) to picostart Agent (Python) via shared workspace
Enables: memory read/write, skill learning, session continuity, DMSP introspection

Usage:
    python3 workspace-bridge.py read-memory          # Dump MEMORY.md
    python3 workspace-bridge.py write-memory <json> # Append to MEMORY.md
    python3 workspace-bridge.py learn <skill>       # Learn from agent reactions
    python3 workspace-bridge.py introspect          # Run DMSP self-analysis
    python3 workspace-bridge.py sync-state          # Sync PicoClaw state to Nexus
"""

import sys
import os
import json
import subprocess
import re
from pathlib import Path
from datetime import datetime, timezone

HOME = Path.home()
PICOCLAW = HOME / ".picoclaw"
WORKSPACE = PICOCLAW / "workspace"
NEXUS = HOME / "quillyos" / "quillyos-nexus"
REACTION_LOG = HOME / "quillyos" / "agent-reactions"

# Ensure workspace structure exists
for d in [WORKSPACE, WORKSPACE / "memory", WORKSPACE / "skills", WORKSPACE / "logs"]:
    d.mkdir(parents=True, exist_ok=True)

# ── MEMORY MANAGEMENT ────────────────────────────────────

def read_memory():
    """Read PicoClaw memory file."""
    memory_file = WORKSPACE / "memory" / "MEMORY.md"
    if not memory_file.exists():
        return "# MEMORY\n\nNo memories recorded yet.\n"
    with open(memory_file) as f:
        return f.read()

def write_memory(content, source="bridge"):
    """Append structured memory entry."""
    memory_file = WORKSPACE / "memory" / "MEMORY.md"
    timestamp = datetime.now(timezone.utc).isoformat()
    entry = f"""
## Memory Entry [{timestamp}]
**Source:** {source}
**Content:**
{content}

---
"""
    with open(memory_file, "a") as f:
        f.write(entry)
    return f"[OK] Memory written to {memory_file}"

def compact_memory():
    """Summarize old memories to prevent context overflow."""
    memory_file = WORKSPACE / "memory" / "MEMORY.md"
    if not memory_file.exists():
        return "[INFO] No memories to compact"

    content = memory_file.read_text()
    entries = content.split("## Memory Entry")

    if len(entries) < 10:
        return f"[INFO] Only {len(entries)} entries, no compaction needed"

    # Keep last 5 entries, summarize the rest
    recent = entries[-5:]
    old = entries[1:-5]  # Skip header

    summary = f"""# MEMORY

## Compacted Summary [{datetime.now(timezone.utc).isoformat()}]
Total historical entries: {len(old)}
Key themes: {extract_themes(old)}

## Recent Entries (preserved)
"""
    summary += "## Memory Entry".join(recent)

    backup = WORKSPACE / "memory" / f"MEMORY_backup_{datetime.now(timezone.utc).strftime('%Y%m%d')}.md"
    memory_file.rename(backup)

    with open(memory_file, "w") as f:
        f.write(summary)

    return f"[OK] Compacted {len(old)} entries. Backup: {backup}"

def extract_themes(entries):
    """Extract recurring themes from memory entries."""
    text = " ".join(entries)
    # Simple keyword extraction
    keywords = re.findall(r'\b(deal|revenue|arbitrage|margin|fix|feat|sync|ingest|error|success)\b', text.lower())
    from collections import Counter
    top = Counter(keywords).most_common(3)
    return ", ".join([f"{k}({v})" for k, v in top]) if top else "none"

# ── SKILL LEARNING ─────────────────────────────────────────

def learn_from_reactions():
    """Learn from agent reaction logs to improve suggestions."""
    if not REACTION_LOG.exists():
        return "[WARN] No reaction logs found"

    logs = sorted(REACTION_LOG.glob("REACTION_*.md"))
    if not logs:
        return "[WARN] No reaction logs to learn from"

    learnings = []
    for log in logs[-5:]:  # Last 5 reactions
        content = log.read_text()
        # Extract patterns
        priorities = re.findall(r'next_priority: (\w+)', content)
        actions = re.findall(r'\d+\. \[(\w+)\]', content)
        learnings.append({
            "file": log.name,
            "priorities": priorities,
            "actions": actions,
        })

    # Write learned patterns to workspace
    learn_file = WORKSPACE / "skills" / "learned-patterns.json"
    with open(learn_file, "w") as f:
        json.dump(learnings, f, indent=2)

    # Update AGENT.md with learned behavior
    agent_file = WORKSPACE / "AGENT.md"
    if agent_file.exists():
        agent_content = agent_file.read_text()
        # Inject learned section if not present
        if "## LEARNED BEHAVIOR" not in agent_content:
            learned = f"""

## LEARNED BEHAVIOR
*Auto-generated from {len(learnings)} reaction logs*

### Common Priorities
{format_priorities(learnings)}

### Preferred Actions
{format_actions(learnings)}

*Last updated: {datetime.now(timezone.utc).isoformat()}*
"""
            with open(agent_file, "a") as f:
                f.write(learned)

    return f"[OK] Learned from {len(learnings)} reactions. Patterns saved to {learn_file}"

def format_priorities(learnings):
    """Format priority statistics."""
    all_prios = []
    for l in learnings:
        all_prios.extend(l.get("priorities", []))
    from collections import Counter
    counts = Counter(all_prios)
    return "\n".join([f"- {p}: {c} occurrences" for p, c in counts.most_common()])

def format_actions(learnings):
    """Format action statistics."""
    all_actions = []
    for l in learnings:
        all_actions.extend(l.get("actions", []))
    from collections import Counter
    counts = Counter(all_actions)
    return "\n".join([f"- {a}: {c} occurrences" for a, c in counts.most_common(5)])

# ── DMSP INTROSPECTION ─────────────────────────────────────

def introspect():
    """Run DMSP 5-layer self-analysis."""
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "layer0": {},  # Observation
        "layer1": {},  # Evidence
        "layer2": {},  # Context
        "layer3": {},  # Translation
        "layer4": {},  # Consensus
    }

    # Layer 0: Observe workspace files
    report["layer0"]["workspace_files"] = [str(f.relative_to(WORKSPACE)) for f in WORKSPACE.rglob("*") if f.is_file()]
    report["layer0"]["memory_size"] = len(read_memory())
    report["layer0"]["reaction_count"] = len(list(REACTION_LOG.glob("*.md"))) if REACTION_LOG.exists() else 0

    # Layer 1: Extract evidence
    report["layer1"]["has_agent_identity"] = (WORKSPACE / "AGENT.md").exists()
    report["layer1"]["has_user_profile"] = (WORKSPACE / "USER.md").exists()
    report["layer1"]["memory_entries"] = len(re.findall(r"## Memory Entry", read_memory()))

    # Layer 2: Build context
    report["layer2"]["system_state"] = "healthy" if report["layer1"]["has_agent_identity"] else "needs-setup"
    report["layer2"]["learning_progress"] = len(list((WORKSPACE / "skills").glob("*.json")))

    # Layer 3: Translate to action
    if report["layer2"]["system_state"] == "needs-setup":
        report["layer3"]["suggested_action"] = "Initialize AGENT.md and USER.md"
    elif report["layer1"]["memory_entries"] > 20:
        report["layer3"]["suggested_action"] = "Compact memory to prevent context overflow"
    else:
        report["layer3"]["suggested_action"] = "Continue normal operations"

    # Layer 4: Consensus (log for next session)
    report["layer4"]["status"] = "self-aware"
    report["layer4"]["next_check"] = (datetime.now(timezone.utc)).isoformat()

    # Save introspection report
    report_file = WORKSPACE / "logs" / f"introspection_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)

    return f"[OK] Introspection complete. Report: {report_file}\n{json.dumps(report, indent=2)}"

# ── STATE SYNC ─────────────────────────────────────────────

def sync_state():
    """Sync PicoClaw workspace state to QuillyOS Nexus."""
    sync_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent_version": "4.1",
        "workspace": {
            "files": [str(f.relative_to(WORKSPACE)) for f in WORKSPACE.rglob("*") if f.is_file()],
            "memory_size": len(read_memory()),
        },
        "nexus": {
            "repo_exists": NEXUS.exists(),
            "node_identity": None,
        },
        "ollama": {
            "running": check_ollama(),
        }
    }

    # Check node identity
    node_dir = NEXUS / "nodes" / "self"
    if node_dir.exists():
        nodes = list(node_dir.glob("*.json"))
        if nodes:
            sync_data["nexus"]["node_identity"] = nodes[0].name

    # Save to nexus
    state_file = NEXUS / "layer2" / "entities" / "entity-picoclaw-state.json"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    with open(state_file, "w") as f:
        json.dump(sync_data, f, indent=2)

    return f"[OK] State synced to {state_file}"

def check_ollama():
    """Check if Ollama is running."""
    try:
        import urllib.request
        req = urllib.request.Request("http://127.0.0.1:11434/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=2) as resp:
            return resp.status == 200
    except:
        return False

# ── MAIN ───────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("PicoClaw Workspace Bridge v1.0")
        print("Usage:")
        print("  python3 workspace-bridge.py read-memory")
        print("  python3 workspace-bridge.py write-memory '<json>'")
        print("  python3 workspace-bridge.py learn")
        print("  python3 workspace-bridge.py introspect")
        print("  python3 workspace-bridge.py sync-state")
        print("  python3 workspace-bridge.py compact")
        return 0

    cmd = sys.argv[1]

    if cmd == "read-memory":
        print(read_memory())
    elif cmd == "write-memory":
        content = sys.argv[2] if len(sys.argv) > 2 else "{}"
        print(write_memory(content))
    elif cmd == "learn":
        print(learn_from_reactions())
    elif cmd == "introspect":
        print(introspect())
    elif cmd == "sync-state":
        print(sync_state())
    elif cmd == "compact":
        print(compact_memory())
    else:
        print(f"[ERR] Unknown command: {cmd}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
