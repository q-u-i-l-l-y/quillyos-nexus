#!/usr/bin/env python3
"""
PicoClaw Agent v4.1 — DMSP Breathing Loop
Natural Language Interface + 5-Layer Introspection
Usage: picostart <command>
"""

import sys
import os
import subprocess
import re
import json
from pathlib import Path
from datetime import datetime, timezone

HOME = Path.home()
NEXUS = HOME / "quillyos" / "quillyos-nexus"
PICOCLAW = HOME / ".picoclaw"
REACTION_LOG = HOME / "quillyos" / "agent-reactions"

# ============================================================
# LAYER 0: OBSERVATION (Raw Data Capture)
# ============================================================

class Layer0Observer:
    """Captures raw system state without interpretation."""

    def observe_git_state(self):
        """Observe current git state."""
        os.chdir(NEXUS)
        head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True).stdout.strip()
        status = subprocess.run(["git", "status", "--short"], capture_output=True, text=True).stdout.strip()
        return {
            "head": head,
            "branch": branch,
            "dirty": bool(status),
            "untracked": status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def observe_commits(self, since_ref):
        """Observe commits since a reference."""
        os.chdir(NEXUS)
        log = subprocess.run(
            ["git", "log", "--oneline", "--stat", f"{since_ref}..HEAD"],
            capture_output=True, text=True
        ).stdout.strip()
        return log

    def observe_files_changed(self, since_ref):
        """Observe which files changed."""
        os.chdir(NEXUS)
        diff = subprocess.run(
            ["git", "diff", "--name-status", f"{since_ref}..HEAD"],
            capture_output=True, text=True
        ).stdout.strip()
        files = []
        for line in diff.split('\n'):
            if line.strip():
                parts = line.split('\t')
                if len(parts) >= 2:
                    files.append({"status": parts[0], "path": parts[1]})
        return files

# ============================================================
# LAYER 1: EVIDENCE (Pattern Extraction)
# ============================================================

class Layer1EvidenceExtractor:
    """Extracts patterns and signals from raw observations."""

    COMMIT_PATTERNS = {
        r"^fix:": {"type": "fix", "priority": "high", "emoji": "🔧", "test_required": True},
        r"^feat:": {"type": "feature", "priority": "medium", "emoji": "✨", "test_required": True},
        r"^docs?:": {"type": "docs", "priority": "low", "emoji": "📄", "test_required": False},
        r"^refactor:": {"type": "refactor", "priority": "medium", "emoji": "♻", "test_required": True},
        r"^chore:": {"type": "chore", "priority": "low", "emoji": "🧹", "test_required": False},
        r"^test:": {"type": "test", "priority": "medium", "emoji": "🧪", "test_required": True},
    }

    PATH_PATTERNS = {
        r"scripts/.*ingest.*": {"component": "ingestor", "layer": "layer1", "critical": True},
        r"scripts/.*": {"component": "script", "layer": "layer3", "critical": False},
        r"entities/.*": {"component": "entity", "layer": "layer2", "critical": True},
        r"contexts/.*": {"component": "context", "layer": "layer2", "critical": True},
        r"protocols/.*": {"component": "protocol", "layer": "layer2", "critical": False},
        r"archive/.*": {"component": "archive", "layer": "layer0", "critical": False},
        r"nodes/.*": {"component": "node", "layer": "layer2", "critical": True},
        r"install/.*": {"component": "installer", "layer": "layer3", "critical": False},
        r"session-briefs/.*": {"component": "brief", "layer": "layer2", "critical": False},
    }

    def extract_commit_evidence(self, commit_line):
        """Extract evidence from a commit line."""
        msg = commit_line.split(' ', 1)[1] if ' ' in commit_line else commit_line
        msg_lower = msg.lower()

        for pattern, evidence in self.COMMIT_PATTERNS.items():
            if re.search(pattern, msg_lower):
                return {**evidence, "message": msg, "raw": commit_line}

        return {"type": "unknown", "priority": "low", "emoji": "❓", "test_required": False, "message": msg, "raw": commit_line}

    def extract_file_evidence(self, file_entry):
        """Extract evidence from a changed file."""
        path = file_entry["path"]
        for pattern, evidence in self.PATH_PATTERNS.items():
            if re.search(pattern, path):
                return {**evidence, "path": path, "change_type": file_entry["status"]}
        return {"component": "unknown", "layer": "unknown", "critical": False, "path": path, "change_type": file_entry["status"]}

    def extract_synthesis(self, commit_evidences, file_evidences):
        """Synthesize cross-layer evidence."""
        # Count by layer
        layer_counts = {}
        for fe in file_evidences:
            layer = fe.get("layer", "unknown")
            layer_counts[layer] = layer_counts.get(layer, 0) + 1

        # Detect critical changes
        critical = any(fe.get("critical") for fe in file_evidences)

        # Detect test requirement
        test_needed = any(ce.get("test_required") for ce in commit_evidences)

        # Detect pattern: fix + critical component = immediate test
        urgent = critical and any(ce["type"] == "fix" for ce in commit_evidences)

        return {
            "layer_distribution": layer_counts,
            "critical_changes": critical,
            "test_required": test_needed,
            "urgent": urgent,
            "commit_count": len(commit_evidences),
            "file_count": len(file_evidences),
        }

# ============================================================
# LAYER 2: CONTEXT (Structured Understanding)
# ============================================================

class Layer2ContextBuilder:
    """Builds structured understanding from evidence."""

    DMSP_LAYERS = {
        "layer0": "Observation — raw data capture",
        "layer1": "Evidence — pattern extraction",
        "layer2": "Context — structured understanding",
        "layer3": "Translation — agent format conversion",
        "layer4": "Consensus — decision & execution",
    }

    ENTITY_MAP = {
        "ingestor": {"entity": "entity-ingestor", "role": "Device scanning and classification"},
        "script": {"entity": "entity-script", "role": "Automation script"},
        "entity": {"entity": "entity-definition", "role": "Canonical knowledge structure"},
        "context": {"entity": "entity-context-matrix", "role": "Mission-specific knowledge package"},
        "protocol": {"entity": "entity-protocol", "role": "System protocol specification"},
        "node": {"entity": "entity-node", "role": "Mesh node identity"},
        "installer": {"entity": "entity-installer", "role": "Clone-to-node onboarding"},
        "brief": {"entity": "entity-session-brief", "role": "Cross-session continuity"},
    }

    def build_context(self, synthesis, file_evidences, commit_evidences):
        """Build contextual understanding of the change."""
        context = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "dmsp_impact": {},
            "entity_impact": [],
            "system_state": {},
            "inference": {},
        }

        # Map layer distribution to DMSP impact
        for layer, count in synthesis.get("layer_distribution", {}).items():
            if layer in self.DMSP_LAYERS:
                context["dmsp_impact"][layer] = {
                    "description": self.DMSP_LAYERS[layer],
                    "files_changed": count,
                }

        # Map components to entities
        for fe in file_evidences:
            comp = fe.get("component", "unknown")
            if comp in self.ENTITY_MAP:
                context["entity_impact"].append({
                    **self.ENTITY_MAP[comp],
                    "path": fe["path"],
                    "change": fe["change_type"],
                })

        # Infer system state implications
        if synthesis.get("urgent"):
            context["system_state"]["stability"] = "potentially-unstable"
            context["system_state"]["action_needed"] = "immediate-verification"
        elif synthesis.get("critical_changes"):
            context["system_state"]["stability"] = "changed"
            context["system_state"]["action_needed"] = "review-and-test"
        else:
            context["system_state"]["stability"] = "stable"
            context["system_state"]["action_needed"] = "optional-review"

        # Infer what the next session needs
        if any(ce["type"] == "fix" for ce in commit_evidences):
            context["inference"]["next_priority"] = "verify-fix"
            context["inference"]["reasoning"] = "A fix was applied. The system must be tested to confirm the bug is resolved and no regressions were introduced."
        elif any(ce["type"] == "feature" for ce in commit_evidences):
            context["inference"]["next_priority"] = "explore-feature"
            context["inference"]["reasoning"] = "New functionality was added. The user should explore capabilities and verify integration with existing components."
        elif any(ce["type"] == "docs" for ce in commit_evidences):
            context["inference"]["next_priority"] = "review-docs"
            context["inference"]["reasoning"] = "Documentation was updated. The user should review new briefs or mappings to understand current priorities."
        else:
            context["inference"]["next_priority"] = "continue"
            context["inference"]["reasoning"] = "Changes are routine. Continue with current priority queue."

        return context

# ============================================================
# LAYER 3: TRANSLATION (Agent Format Conversion)
# ============================================================

class Layer3Translator:
    """Translates context into actionable suggestions."""

    def translate(self, context, synthesis, reporter):
        """Translate context into user-facing suggestions."""
        reporter.banner("DMSP BREATHING LOOP")
        reporter.say("Running 5-layer introspection...", "action")

        # Layer 0 report
        reporter.say("Layer 0 (Observation): Detected new commits on mesh", "info")
        reporter.say(f"  Commits: {synthesis['commit_count']}, Files: {synthesis['file_count']}", "info")

        # Layer 1 report
        reporter.say("Layer 1 (Evidence): Extracting patterns...", "info")
        if synthesis["critical_changes"]:
            reporter.say("  ⚠ Critical components were modified", "warn")
        if synthesis["test_required"]:
            reporter.say("  🧪 Testing is recommended", "warn")
        if synthesis["urgent"]:
            reporter.say("  🚨 URGENT: Fix applied to critical component", "warn")

        # Layer 2 report
        reporter.say("Layer 2 (Context): Building understanding...", "info")
        for layer, info in context["dmsp_impact"].items():
            reporter.say(f"  {layer}: {info['description']} ({info['files_changed']} files)", "info")

        if context["entity_impact"]:
            reporter.say("  Entity impact:", "info")
            for ei in context["entity_impact"][:3]:
                reporter.say(f"    {ei['entity']} ({ei['role']}) — {ei['change']}", "info")

        # Layer 3 report (Translation to action)
        reporter.say("Layer 3 (Translation): Converting to actions...", "info")

        actions = []
        priority = context["inference"]["next_priority"]

        if priority == "verify-fix":
            actions.append(("Test the fixed component", 'picostart "ingest my documents folder"', "high"))
            actions.append(("Check for regressions", 'picostart "show me my status"', "medium"))
        elif priority == "explore-feature":
            actions.append(("Try the new feature", "Read the commit diff to understand usage", "high"))
            actions.append(("Run a full scan", 'picostart "ingest my documents folder"', "medium"))
        elif priority == "review-docs":
            actions.append(("Read updated documentation", f"cat {NEXUS}/session-briefs/SESSION_BRIEF_*.md", "medium"))
            actions.append(("Continue with priority queue", "Review PRIORITY QUEUE in latest brief", "low"))
        else:
            actions.append(("Continue current work", "Proceed with next priority item", "low"))

        # Always offer sync as baseline
        actions.append(("Sync local state", 'picostart "sync with the mesh"', "low"))

        reporter.say("Layer 4 (Consensus): Awaiting your decision...", "info")
        reporter.say(f"  Inference: {context['inference']['reasoning']}", "info")
        reporter.say("", "info")
        reporter.say("Suggested actions:", "ask")

        for i, (desc, cmd, prio) in enumerate(actions, 1):
            emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(prio, "•")
            reporter.say(f"  {emoji} {i}. {desc}", "action")
            reporter.say(f"     → {cmd}", "info")

        return actions

# ============================================================
# LAYER 4: CONSENSUS (Decision & Execution)
# ============================================================

class Layer4Consensus:
    """Presents options and logs the reaction for next session."""

    def __init__(self):
        REACTION_LOG.mkdir(parents=True, exist_ok=True)

    def log_reaction(self, context, synthesis, actions, before, after):
        """Write reaction log for next Kimi session."""
        timestamp = datetime.now(timezone.utc)
        filename = f"REACTION_{timestamp.strftime('%Y%m%d_%H%M%S')}.md"
        path = REACTION_LOG / filename

        lines = [
            f"# Agent Reaction Log (DMSP Introspection)",
            f"**Generated:** {timestamp.isoformat()}",
            f"**Range:** {before[:7]} → {after[:7]}",
            f"",
            f"## Layer 0: Observation",
            f"- Commits detected: {synthesis['commit_count']}",
            f"- Files changed: {synthesis['file_count']}",
            f"- Critical changes: {synthesis['critical_changes']}",
            f"",
            f"## Layer 1: Evidence",
            f"- Urgent: {synthesis['urgent']}",
            f"- Test required: {synthesis['test_required']}",
            f"- Layer distribution: {json.dumps(synthesis['layer_distribution'])}",
            f"",
            f"## Layer 2: Context",
            f"- System stability: {context['system_state']['stability']}",
            f"- Action needed: {context['system_state']['action_needed']}",
            f"- Next priority: {context['inference']['next_priority']}",
            f"- Reasoning: {context['inference']['reasoning']}",
            f"",
            f"## Layer 3: Translation (Suggested Actions)",
        ]

        for i, (desc, cmd, prio) in enumerate(actions, 1):
            lines.append(f"{i}. [{prio.upper()}] {desc} → `{cmd}`")

        lines.extend([
            f"",
            f"## Layer 4: Consensus",
            f"Status: Awaiting user input",
            f"",
            f"## For Next Kimi Session",
            f"",
            f"The agent performed DMSP introspection and is waiting for user consensus.",
            f"To continue: run one of the suggested actions, observe the output,",
            f"and paste the transcript for the next Kimi session.",
            f"",
            f"---",
            f"*Auto-generated by PicoClaw Agent v4.1 (DMSP Breathing Loop)*",
        ])

        with open(path, 'w') as f:
            f.write('\n'.join(lines))

        return path

# ============================================================
# BREATHING LOOP ORCHESTRATOR
# ============================================================

class BreathingLoop:
    """Orchestrates the 5-layer DMSP breathing loop."""

    def __init__(self, reporter):
        self.reporter = reporter
        self.l0 = Layer0Observer()
        self.l1 = Layer1EvidenceExtractor()
        self.l2 = Layer2ContextBuilder()
        self.l3 = Layer3Translator()
        self.l4 = Layer4Consensus()

    def breathe(self):
        """Execute one full breathing cycle."""
        self.reporter.banner("BREATHING LOOP")
        self.reporter.say("Inhaling from mesh...", "action")

        os.chdir(NEXUS)

        # Get baseline
        before = self.l0.observe_git_state()["head"]

        # Pull
        pull = subprocess.run(["git", "pull", "origin", "main"], capture_output=True, text=True)

        if "Already up to date" in pull.stdout:
            self.reporter.say("Mesh is current. No new breath needed.", "ok")
            # Still do a shallow introspection of local state
            self._introspect_local()
            return 0

        # Get new state
        after = self.l0.observe_git_state()["head"]

        if before == after:
            self.reporter.say("Pull completed but HEAD unchanged.", "warn")
            return 0

        # Layer 0: Observe commits and files
        commit_log = subprocess.run(["git", "log", "--oneline", f"{before}..{after}"], capture_output=True, text=True).stdout.strip()
        commits = [c for c in commit_log.split('\n') if c.strip()]
        files = self.l0.observe_files_changed(before)

        # Layer 1: Extract evidence
        commit_evidences = [self.l1.extract_commit_evidence(c) for c in commits]
        file_evidences = [self.l1.extract_file_evidence(f) for f in files]
        synthesis = self.l1.extract_synthesis(commit_evidences, file_evidences)

        # Layer 2: Build context
        context = self.l2.build_context(synthesis, file_evidences, commit_evidences)

        # Layer 3: Translate to actions
        actions = self.l3.translate(context, synthesis, self.reporter)

        # Layer 4: Log for consensus
        log_path = self.l4.log_reaction(context, synthesis, actions, before, after)
        self.reporter.say(f"Reaction logged: {log_path}", "ok")

        self.reporter.say("Exhale complete. Awaiting your consensus.", "done")
        return 0

    def _introspect_local(self):
        """Shallow introspection when no new commits."""
        self.reporter.say("Running shallow introspection of local state...", "info")

        # Check for uncommitted local changes
        os.chdir(NEXUS)
        status = subprocess.run(["git", "status", "--short"], capture_output=True, text=True).stdout.strip()

        if status:
            self.reporter.say("You have uncommitted local changes:", "warn")
            for line in status.split('\n')[:5]:
                self.reporter.say(f"  {line}", "info")
            self.reporter.say('Say "sync" to push these to the mesh', "action")
        else:
            self.reporter.say("Local state is clean. Nexus is in equilibrium.", "ok")

        # Check node identity
        node_files = list((NEXUS / "nodes" / "self").glob("*.json"))
        if node_files:
            self.reporter.say(f"Node identity: {node_files[0].name}", "ok")
        else:
            self.reporter.say("No node identity found. Run 'picostart register'.", "warn")

# ============================================================
# PLAIN LANGUAGE REPORTER
# ============================================================

class PlainLanguageReporter:
    def say(self, message, level="info"):
        prefixes = {
            "info": "🤖",
            "ok": "✓",
            "warn": "⚠",
            "ask": "❓",
            "action": "→",
            "done": "🎉",
        }
        print(f"  {prefixes.get(level, '•')} {message}")

    def banner(self, title):
        print(f"\n{'='*50}")
        print(f"  {title}")
        print(f"{'='*50}")

# ============================================================
# NATURAL LANGUAGE PARSER
# ============================================================

class PlainLanguageParser:
    INGEST_PATTERNS = [
        r"ingest\s+(?:my\s+)?(.+)",
        r"scan\s+(?:my\s+)?(.+)",
        r"check\s+(?:my\s+)?(.+)",
        r"organize\s+(?:my\s+)?(.+)",
        r"classify\s+(?:my\s+)?(.+)",
        r"what(?:'s)?\s+in\s+(?:my\s+)?(.+)",
        r"show\s+me\s+(?:my\s+)?(.+)",
    ]
    SYNC_PATTERNS = [
        r"sync",
        r"push\s+to\s+(?:the\s+)?mesh",
        r"commit\s+and\s+push",
        r"update\s+(?:the\s+)?repo",
        r"send\s+to\s+github",
    ]
    STATUS_PATTERNS = [
        r"status",
        r"what(?:'s)?\s+up",
        r"show\s+me\s+status",
        r"check\s+status",
        r"what\s+do\s+you\s+see",
    ]
    START_PATTERNS = [r"start", r"launch", r"run", r"begin"]
    WATCH_PATTERNS = [
        r"watch", r"check.*update", r"pull.*react", r"what.*changed",
        r"react.*commit", r"breathing.*loop", r"mesh.*status", r"breathe",
        r"introspect", r"analyze.*mesh", r"what.*new",
    ]

    TARGET_MAP = {
        "documents": ["/storage/emulated/0/Documents", HOME / "Documents"],
        "downloads": ["/storage/emulated/0/Download", HOME / "Download"],
        "home": [str(HOME)],
        "quillyos": [str(HOME / "quillyos")],
        "termux": [str(HOME)],
        "device": ["/storage/emulated/0"],
        "everything": [str(HOME), "/storage/emulated/0/Documents", "/storage/emulated/0/Download"],
        "nexus": [str(NEXUS)],
        "repo": [str(NEXUS)],
    }

    def parse(self, text):
        text = text.lower().strip()

        for pattern in self.WATCH_PATTERNS:
            if re.search(pattern, text):
                return {"intent": "watch", "target": str(NEXUS), "original": text}

        for pattern in self.INGEST_PATTERNS:
            match = re.search(pattern, text)
            if match:
                target = self.resolve_target(match.group(1).strip())
                return {"intent": "ingest", "target": target, "original": text}

        for pattern in self.SYNC_PATTERNS:
            if re.search(pattern, text):
                return {"intent": "sync", "target": str(NEXUS), "original": text}

        for pattern in self.STATUS_PATTERNS:
            if re.search(pattern, text):
                return {"intent": "status", "target": str(NEXUS), "original": text}

        for pattern in self.START_PATTERNS:
            if re.search(pattern, text):
                return {"intent": "start", "target": None, "original": text}

        return {"intent": "unknown", "target": None, "original": text}

    def resolve_target(self, target_str):
        target_str = target_str.lower().strip()
        if target_str.startswith("/") or target_str.startswith("~"):
            return os.path.expanduser(target_str)
        for alias, paths in self.TARGET_MAP.items():
            if alias in target_str:
                for p in paths:
                    if os.path.exists(p):
                        return p
                return str(paths[0])
        return str(HOME)

# ============================================================
# ACTION HANDLERS
# ============================================================

def handle_ingest(target, reporter):
    reporter.banner("PICOCLAW AGENT")
    reporter.say(f"Launching ingest scan of: {target}", "action")
    ingestor = NEXUS / "scripts" / "nexus-ingest.py"
    if not ingestor.exists():
        reporter.say("Ingestor not found. Checking alternatives...", "warn")
        for path in [
            HOME / "quillyos" / "quillyos-nexus" / "scripts" / "nexus-ingest.py",
            HOME / "picoclaw-dev" / "document_ingestor_v2.1.py",
        ]:
            if path.exists():
                reporter.say(f"Found ingestor at: {path}", "ok")
                ingestor = path
                break
        else:
            reporter.say("No ingestor found. Please run setup first.", "warn")
            return 1

    reporter.say("Scanning your device... this may take a minute.", "info")
    result = subprocess.run([sys.executable, str(ingestor)], capture_output=True, text=True)

    if result.returncode == 0:
        reporter.say("Scan complete!", "done")
        report_path = HOME / "quillyos" / "ingest-report.json"
        if report_path.exists():
            with open(report_path) as f:
                data = json.load(f)
            summary = data.get("summary", {})
            total = sum(summary.values())
            reporter.say(f"Scanned {total} files total.", "info")
            for cat, count in summary.items():
                if count > 0:
                    reporter.say(f"  {cat}: {count}", "info")
            reporter.say("\nWhat would you like me to do next?", "ask")
            if summary.get("commit_to_nexus", 0) > 0:
                reporter.say('  Say "stage them" to prepare for commit', "action")
            if summary.get("archive", 0) > 0:
                reporter.say('  Say "archive them" to move legacy files', "action")
        else:
            reporter.say("Scan finished but report file not found.", "warn")
    else:
        reporter.say(f"Scan failed: {result.stderr[:200]}", "warn")
    return 0

def handle_sync(reporter):
    reporter.banner("SYNC WITH MESH")
    reporter.say("Pulling latest from GitHub...", "action")
    os.chdir(NEXUS)
    subprocess.run(["git", "pull", "origin", "main"])
    reporter.say("Checking for local changes...", "info")
    result = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
    if result.stdout.strip():
        reporter.say("Found local changes. Committing...", "action")
        subprocess.run(["git", "add", "-A"])
        subprocess.run(["git", "commit", "-m", f"sync: {datetime.now(timezone.utc).isoformat()}Z"])
        subprocess.run(["git", "push", "origin", "main"])
        reporter.say("Synced with mesh!", "done")
    else:
        reporter.say("Everything is up to date.", "ok")
    return 0

def handle_status(reporter):
    reporter.banner("STATUS")
    os.chdir(NEXUS)
    result = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
    if result.stdout.strip():
        reporter.say("You have uncommitted changes:", "warn")
        for line in result.stdout.strip().split('\n')[:10]:
            reporter.say(f"  {line}", "info")
        reporter.say("\nSay 'sync' to push these to the mesh.", "action")
    else:
        reporter.say("Nexus is clean. Nothing to commit.", "ok")
    node_files = list((NEXUS / "nodes" / "self").glob("*.json"))
    if node_files:
        reporter.say(f"Your node: {node_files[0].name}", "ok")
    else:
        reporter.say("No node identity found. Run 'picostart register'.", "warn")
    return 0

def handle_start(reporter):
    reporter.banner("STARTING BRIDGE")
    bridge = PICOCLAW / "hybrid-system-v3" / "picoclaw_bridge" / "hybrid_bridge.py"
    if bridge.exists():
        reporter.say(f"Launching bridge: {bridge}", "action")
        subprocess.run([sys.executable, str(bridge)])
    else:
        reporter.say("Bridge not found.", "warn")
    return 0

def handle_watch(reporter):
    loop = BreathingLoop(reporter)
    return loop.breathe()

# ============================================================
# MAIN
# ============================================================

def main():
    if len(sys.argv) < 2:
        print("PicoClaw Agent v4.1 — DMSP Breathing Loop")
        print("Usage: picostart <command>")
        print("")
        print("Natural language:")
        print('  picostart "ingest my documents folder"')
        print('  picostart "sync with the mesh"')
        print('  picostart "show me my status"')
        print('  picostart "check for updates"   ← DMSP breathing loop')
        print('  picostart "breathe"             ← DMSP introspection')
        print("")
        print("Shorthand:")
        print("  picostart sync")
        print("  picostart status")
        print("  picostart watch")
        return 0

    command = " ".join(sys.argv[1:])
    parser = PlainLanguageParser()
    reporter = PlainLanguageReporter()
    intent = parser.parse(command)

    if intent["intent"] == "ingest":
        return handle_ingest(intent["target"], reporter)
    elif intent["intent"] == "sync":
        return handle_sync(reporter)
    elif intent["intent"] == "status":
        return handle_status(reporter)
    elif intent["intent"] == "start":
        return handle_start(reporter)
    elif intent["intent"] == "watch":
        return handle_watch(reporter)
    else:
        reporter.say(f"I didn't understand: '{command}'", "warn")
        reporter.say("Try saying:", "info")
        reporter.say('  "ingest my documents folder"', "action")
        reporter.say('  "sync with the mesh"', "action")
        reporter.say('  "show me my status"', "action")
        reporter.say('  "check for updates"', "action")
        return 1

if __name__ == "__main__":
    sys.exit(main())
