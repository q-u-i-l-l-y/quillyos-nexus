#!/usr/bin/env python3
"""
QUILLYOS // NEXUS INGEST v4.0
Device Assessment & Classification Engine

Scans Termux home, quillyos directories, and device Documents.
Classifies every file into: commit-to-nexus | merge-required | archive | personal | unknown
Reports in plain language. Interactive mode for ambiguous cases.

Usage:
    python3 nexus-ingest.py [--scan-path PATH] [--non-interactive] [--output-json]
"""

import os
import sys
import json
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
from fnmatch import fnmatch

# ── CONFIG ─────────────────────────────────────────────────
EXCLUDE_PATTERNS = [
    "*.tmp", "*.cache", "__pycache__", ".git", ".venv", "venv",
    "*.log", "*.pid", "node_modules", ".termux", ".cache",
    "*.pyc", ".DS_Store", "Thumbs.db", "*.swp", "*.swo"
]

# Classification keywords
NEXUS_KEYWORDS = [
    "quillyos", "nexus", "picoclaw", "protocol", "matrix",
    "entity", "observation", "evidence", "context", "consensus",
    "revenue", "arbitrage", "wholesale", "ENDS", "metamaterial",
    "quantum", "biotech", "nanotech", "health", "sensor",
    "bootstrap", "vision", "north star", "mission", "doctrine",
    "knowledge", "superposition", "mesh", "node", "spoke", "hub"
]

LEGACY_KEYWORDS = [
    "phone_bootstrap", "legacy", "deprecated", "old version",
    "superseded", "archive", "backup", "old_"
]

PERSONAL_PATTERNS = [
    "*.jpg", "*.jpeg", "*.png", "*.gif", "*.mp4", "*.mp3",
    "*.wav", "*.pdf", "*.epub", "*.docx", "*.xlsx",
    "*personal*", "*private*", "*photo*", "*music*", "*video*",
    "*family*", "*finance_personal*", "*tax*"
]

# ── PLAIN LANGUAGE OUTPUT ──────────────────────────────────
class PlainLanguageReporter:
    """Speaks human about what the scanner found."""

    def __init__(self, verbose=True, interactive=True):
        self.verbose = verbose
        self.interactive = interactive
        self.results = {
            "commit_to_nexus": [],
            "merge_required": [],
            "archive": [],
            "personal": [],
            "unknown": [],
            "errors": []
        }
        self.stats = {"scanned": 0, "bytes": 0, "dirs": 0}

    def say(self, text, level="info"):
        """Print with visual hierarchy."""
        prefix = {
            "info": "[INFO]",
            "warn": "[WARN]",
            "ok": "[OK]  ",
            "ask": "[ASK] ",
            "scan": "[SCAN]",
            "found": "[FOUND]",
            "skip": "[SKIP]"
        }.get(level, "[INFO]")
        if self.verbose or level in ("warn", "ask", "ok"):
            print(f"  {prefix} {text}")

    def banner(self, title):
        print(f"\n{'='*50}")
        print(f"  {title}")
        print(f"{'='*50}")

    def classify_file(self, path, content_sample=""):
        """Classify a single file. Returns category + reason."""
        name = path.name.lower()

        # Personal first — strongest exclusion
        for pat in PERSONAL_PATTERNS:
            if fnmatch(name, pat):
                return "personal", f"matches personal pattern: {pat}"

        # Legacy / archive
        for kw in LEGACY_KEYWORDS:
            if kw in name or kw in content_sample.lower():
                return "archive", f"legacy keyword detected: '{kw}'"

        # Nexus-relevant by name
        for kw in NEXUS_KEYWORDS:
            if kw in name:
                return "commit_to_nexus", f"nexus keyword in filename: '{kw}'"

        # Nexus-relevant by content
        content_lower = content_sample.lower()
        nexus_matches = [kw for kw in NEXUS_KEYWORDS if kw in content_lower]
        if len(nexus_matches) >= 3:
            return "commit_to_nexus", f"nexus content keywords: {', '.join(nexus_matches[:3])}"
        if len(nexus_matches) >= 1:
            return "merge_required", f"some nexus keywords: {', '.join(nexus_matches[:2])}"

        # README, LICENSE, config files — likely merge
        if name.startswith("readme") or name.startswith("license") or name.startswith("config"):
            return "merge_required", f"standard file type: {name}"

        # Code files in quillyos directories
        if "quillyos" in str(path).lower() and name.endswith((".py", ".sh", ".json", ".md", ".yaml", ".yml")):
            return "commit_to_nexus", f"code file in quillyos directory"

        # Unknown — needs review
        return "unknown", "no clear classification signals"

    def ask_human(self, path, current_guess, reason):
        """Interactive prompt for ambiguous files."""
        if not self.interactive:
            return current_guess

        print(f"\n  {'─'*40}")
        print(f"  FILE: {path}")
        print(f"  GUESS: {current_guess} — {reason}")
        print(f"  {'─'*40}")
        print("  What should I do?")
        print("    [c] commit to nexus")
        print("    [m] merge with existing (review needed)")
        print("    [a] archive (preserve but don't merge)")
        print("    [p] personal — skip")
        print("    [s] skip for now")
        print("    [Enter] accept guess: {}".format(current_guess))

        try:
            choice = input("  > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            choice = ""

        mapping = {
            "c": "commit_to_nexus",
            "m": "merge_required",
            "a": "archive",
            "p": "personal",
            "s": "unknown",
            "": current_guess
        }
        return mapping.get(choice, current_guess)

    def scan_directory(self, root_path, label=""):
        """Scan a directory tree and classify all files."""
        root = Path(root_path).expanduser()
        if not root.exists():
            self.say(f"Path not found: {root}", "warn")
            return

        self.banner(f"SCANNING: {label or root}")

        for path in root.rglob("*"):
            # Skip excluded patterns
            rel = str(path.relative_to(root))
            skip = False
            for pat in EXCLUDE_PATTERNS:
                if fnmatch(rel, pat) or any(fnmatch(p, pat) for p in path.parts):
                    skip = True
                    break
            if skip:
                continue

            if path.is_dir():
                self.stats["dirs"] += 1
                continue

            self.stats["scanned"] += 1
            try:
                self.stats["bytes"] += path.stat().st_size
            except:
                pass

            # Read content sample (first 4KB of text files)
            content_sample = ""
            try:
                if path.stat().st_size < 1024 * 1024:  # Skip files > 1MB
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content_sample = f.read(4096)
            except:
                pass

            category, reason = self.classify_file(path, content_sample)

            # Interactive override for unknown or merge_required
            if self.interactive and category in ("unknown", "merge_required"):
                category = self.ask_human(path, category, reason)

            self.results[category].append({
                "path": str(path),
                "relative": rel,
                "size": path.stat().st_size if path.exists() else 0,
                "reason": reason,
                "content_hash": hashlib.sha256(content_sample.encode()).hexdigest()[:16] if content_sample else ""
            })

            if self.verbose and len(self.results[category]) <= 5:
                self.say(f"{category}: {rel}", "found")

    def generate_report(self):
        """Generate plain language summary."""
        self.banner("ASSESSMENT COMPLETE")

        total = self.stats["scanned"]
        print(f"\n  Scanned: {total} files across {self.stats['dirs']} directories")
        print(f"  Total size: {self.stats['bytes'] / 1024 / 1024:.1f} MB")

        print(f"\n  {'─'*40}")
        print(f"  CLASSIFICATION RESULTS")
        print(f"  {'─'*40}")

        for cat, items in self.results.items():
            if not items:
                continue

            labels = {
                "commit_to_nexus": ("COMMIT TO NEXUS", "These files belong in the repo"),
                "merge_required": ("MERGE REQUIRED", "These overlap with existing content — review needed"),
                "archive": ("ARCHIVE", "Legacy files — preserve but don't merge into nexus"),
                "personal": ("PERSONAL", "Private files — skip"),
                "unknown": ("UNKNOWN", "Needs human review")
            }
            label, desc = labels.get(cat, (cat.upper(), ""))

            print(f"\n  📁 {label} ({len(items)} files)")
            print(f"     {desc}")
            for item in items[:5]:
                size_kb = item["size"] / 1024
                print(f"     • {item['relative']} ({size_kb:.1f} KB)")
            if len(items) > 5:
                print(f"     ... and {len(items) - 5} more")

        # Recommendations
        print(f"\n  {'─'*40}")
        print(f"  RECOMMENDATIONS")
        print(f"  {'─'*40}")

        commit_count = len(self.results["commit_to_nexus"])
        merge_count = len(self.results["merge_required"])
        archive_count = len(self.results["archive"])

        if commit_count > 0:
            print(f"  → Stage {commit_count} files for commit to quillyos-nexus")
        if merge_count > 0:
            print(f"  → Review {merge_count} files for merge with existing nexus content")
        if archive_count > 0:
            print(f"  → Move {archive_count} legacy files to archive/")

        print(f"\n  Next steps:")
        print(f"    1. Review the 'MERGE REQUIRED' list carefully")
        print(f"    2. Run with --output-json to save this report")
        print(f"    3. Commit approved files: nexus-commit")
        print(f"    4. Archive legacy files in picoclaw-dev/archive/")

    def save_json(self, output_path):
        """Save full report as JSON."""
        report = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "node_id": "auto-detect",
            "stats": self.stats,
            "results": self.results
        }
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n  [OK] Report saved: {output_path}")


# ── MAIN ─────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Nexus Device Ingest & Classification")
    parser.add_argument("--scan-path", default="$HOME", help="Root path to scan (default: $HOME)")
    parser.add_argument("--non-interactive", action="store_true", help="Skip interactive prompts")
    parser.add_argument("--output-json", default="", help="Save report to JSON file")
    parser.add_argument("--quiet", action="store_true", help="Minimal output")
    args = parser.parse_args()

    reporter = PlainLanguageReporter(
        verbose=not args.quiet,
        interactive=not args.non_interactive
    )

    # Scan multiple key locations
    scan_paths = [
        ("$HOME", "Termux Home"),
        ("$HOME/quillyos", "QuillyOS Directory"),
        ("/storage/emulated/0/Documents", "Device Documents"),
        ("/storage/emulated/0/Download", "Device Downloads"),
    ]

    for path, label in scan_paths:
        reporter.scan_directory(path, label)

    reporter.generate_report()

    if args.output_json:
        reporter.save_json(args.output_json)

    # Return summary for scripting
    summary = {
        "commit": len(reporter.results["commit_to_nexus"]),
        "merge": len(reporter.results["merge_required"]),
        "archive": len(reporter.results["archive"]),
        "personal": len(reporter.results["personal"]),
        "unknown": len(reporter.results["unknown"])
    }

    if args.output_json:
        print(f"\n  Summary: {json.dumps(summary)}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
