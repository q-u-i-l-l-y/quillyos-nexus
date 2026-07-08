#!/usr/bin/env python3
"""
nexus-ingest.py v4.0 — Stable Ingestor with Classification Engine
Scans device locations, classifies files, generates ingest-report.json

Usage:
    python3 nexus-ingest.py                          # Scan default locations
    python3 nexus-ingest.py /path/to/scan            # Scan specific path
    python3 nexus-ingest.py /path/1 /path/2          # Scan multiple paths
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime, timezone

HOME = Path.home()
NEXUS = HOME / "quillyos" / "quillyos-nexus"
REPORT_PATH = HOME / "quillyos" / "ingest-report.json"

# Default scan locations
DEFAULT_LOCATIONS = [
    "/storage/emulated/0/Documents",
    "/storage/emulated/0/Download",
    str(HOME / "Documents"),
    str(HOME),
]

# Classification patterns — ordered by priority
NEXUS_PATTERNS = [
    r"quillyos", r"nexus", r"picoclaw", r"vision", r"brief",
    r"entity", r"protocol", r"matrix", r"doctrine", r"north.?star",
    r"\.md$", r"\.py$", r"\.json$", r"\.sh$", r"\.yaml$", r"\.yml$",
    r"\.txt$", r"\.toml$", r"Makefile", r"Dockerfile", r"\.gitignore",
]

ARCHIVE_PATTERNS = [
    r"_old", r"_backup", r"_archive", r"legacy", r"deprecated",
    r"\.bak$", r"\.old$", r"\.backup$", r"archive",
]

PERSONAL_PATTERNS = [
    r"\.jpg$", r"\.jpeg$", r"\.png$", r"\.gif$", r"\.mp4$",
    r"\.mp3$", r"\.avi$", r"\.mov$", r"\.wav$", r"\.heic$",
    r"private", r"personal", r"secret", r"\.zip$", r"\.rar$",
]

SKIP_NAMES = {".git", "node_modules", "__pycache__", ".pytest_cache", "Thumbs.db", "desktop.ini", ".DS_Store"}


def classify_file(path):
    """Classify a single file path into a category."""
    name = path.name.lower()
    str_path = str(path).lower()

    if any(part in SKIP_NAMES for part in path.parts):
        return None

    # Personal media / private
    for p in PERSONAL_PATTERNS:
        if re.search(p, name) or re.search(p, str_path):
            return "personal"

    # Archive / legacy
    for p in ARCHIVE_PATTERNS:
        if re.search(p, name) or re.search(p, str_path):
            return "archive"

    # Nexus-related / project files
    for p in NEXUS_PATTERNS:
        if re.search(p, name) or re.search(p, str_path):
            # Check if filename already exists somewhere in nexus
            for existing in NEXUS.rglob(path.name):
                if existing.is_file():
                    return "merge_required"
            return "commit_to_nexus"

    return "unknown"


def scan_location(location):
    """Scan a single location and return classified files."""
    results = {
        "commit_to_nexus": [],
        "merge_required": [],
        "archive": [],
        "personal": [],
        "unknown": [],
    }
    path = Path(location)
    if not path.exists():
        return results

    try:
        for item in path.rglob("*"):
            if item.is_file():
                cat = classify_file(item)
                if cat and cat in results:
                    results[cat].append(str(item))
    except PermissionError:
        pass
    return results


def merge_results(a, b):
    """Merge two result dicts."""
    for key in a:
        a[key].extend(b.get(key, []))
    return a


def deduplicate_results(results):
    """Remove duplicate paths while preserving order."""
    for key in results:
        seen = set()
        deduped = []
        for p in results[key]:
            if p not in seen:
                seen.add(p)
                deduped.append(p)
        results[key] = deduped
    return results


def scan_device(targets=None):
    """Main scan function. Returns 0 on success."""
    if targets is None:
        targets = DEFAULT_LOCATIONS
    elif isinstance(targets, str):
        targets = [targets]

    all_results = {
        "commit_to_nexus": [],
        "merge_required": [],
        "archive": [],
        "personal": [],
        "unknown": [],
    }

    for loc in targets:
        loc_path = Path(loc)
        if loc_path.exists():
            res = scan_location(loc)
            all_results = merge_results(all_results, res)
        else:
            print(f"[WARN] Location not found: {loc}")

    all_results = deduplicate_results(all_results)

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "scanner_version": "4.0",
        "targets": targets,
        "results": all_results,
        "summary": {k: len(v) for k, v in all_results.items()},
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print(f"[OK] Scan complete. Report: {REPORT_PATH}")
    print(f"Summary: {json.dumps(report['summary'], indent=2)}")
    return 0


if __name__ == "__main__":
    targets = sys.argv[1:] if len(sys.argv) > 1 else None
    sys.exit(scan_device(targets))
