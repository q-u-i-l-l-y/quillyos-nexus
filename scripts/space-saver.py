#!/usr/bin/env python3
"""
Ollama Space Saver for Termux
Identifies what can be safely deleted to free up disk space
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime, timezone

HOME = Path.home()
OLLAMA = HOME / ".ollama"
MODELS = OLLAMA / "models"
BLOBS = MODELS / "blobs"
MANIFESTS = MODELS / "manifests"

def analyze_space():
    """Analyze what's taking space in Ollama."""
    print("=" * 60)
    print("OLLAMA SPACE ANALYSIS")
    print("=" * 60)

    # Total Ollama size
    total_size = get_dir_size(OLLAMA)
    print(f"\nTotal Ollama directory: {total_size / (1024**3):.2f} GB")

    # Blobs breakdown
    print("\n--- BLOBS (model weights) ---")
    if BLOBS.exists():
        blobs = sorted(BLOBS.glob("sha256-*"), key=lambda x: x.stat().st_size, reverse=True)
        total_blobs = 0
        for blob in blobs:
            size = blob.stat().st_size
            total_blobs += size
            print(f"  {blob.name[:30]}... {size / (1024**2):.1f} MB")
        print(f"  Total blobs: {total_blobs / (1024**3):.2f} GB")

    # Manifests
    print("\n--- MANIFESTS (metadata) ---")
    if MANIFESTS.exists():
        manifest_size = get_dir_size(MANIFESTS)
        print(f"  Total: {manifest_size / 1024:.1f} KB (negligible)")

    # Cache
    cache = OLLAMA / "cache"
    print("\n--- CACHE ---")
    if cache.exists():
        cache_size = get_dir_size(cache)
        print(f"  Total: {cache_size / (1024**2):.1f} MB")
        print(f"  [SAFE TO DELETE] Run: rm -rf ~/.ollama/cache")

    # History
    history = OLLAMA / "history"
    print("\n--- HISTORY ---")
    if history.exists():
        hist_size = get_dir_size(history)
        print(f"  Total: {hist_size / 1024:.1f} KB")
        print(f"  [SAFE TO DELETE] Run: rm -rf ~/.ollama/history")

    # Logs
    logs = OLLAMA / "logs"
    print("\n--- LOGS ---")
    if logs.exists():
        log_size = get_dir_size(logs)
        print(f"  Total: {log_size / (1024**2):.1f} MB")
        print(f"  [SAFE TO DELETE] Run: rm -rf ~/.ollama/logs")

    # Old models
    print("\n--- OLD MODELS (can be removed) ---")
    old_models = find_old_models()
    for model in old_models:
        print(f"  {model['name']}: {model['size'] / (1024**3):.2f} GB")
        print(f"    [DELETE] ollama rm {model['name']}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Safe to delete:")
    print(f"  - Cache: ~{cache_size / (1024**2):.0f} MB")
    print(f"  - History: ~{hist_size / 1024:.0f} KB")
    print(f"  - Logs: ~{log_size / (1024**2):.0f} MB")
    print(f"  - Old models: ~{sum(m['size'] for m in old_models) / (1024**3):.2f} GB")

    return {
        "cache": cache_size,
        "history": hist_size,
        "logs": log_size,
        "old_models": old_models,
    }

def get_dir_size(path):
    """Get total size of directory."""
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += get_dir_size(entry.path)
    return total

def find_old_models():
    """Find models that can be safely removed."""
    old = []

    # Check for qwen2.5:0.5b (replaced by 3.5)
    qwen25 = MANIFESTS / "registry.ollama.ai" / "library" / "qwen2.5"
    if qwen25.exists():
        for manifest in qwen25.glob("*"):
            if manifest.is_file():
                with open(manifest) as f:
                    data = json.load(f)
                size = sum(l.get("size", 0) for l in data.get("layers", []))
                old.append({"name": f"qwen2.5:{manifest.name}", "size": size})

    # Check for qwen3:1.7b (if pulled and not needed)
    qwen3 = MANIFESTS / "registry.ollama.ai" / "library" / "qwen3"
    if qwen3.exists():
        for manifest in qwen3.glob("*"):
            if manifest.is_file() and "1.7b" in manifest.name:
                with open(manifest) as f:
                    data = json.load(f)
                size = sum(l.get("size", 0) for l in data.get("layers", []))
                old.append({"name": f"qwen3:{manifest.name}", "size": size})

    return old

def safe_cleanup():
    """Perform safe cleanup."""
    print("\n" + "=" * 60)
    print("PERFORMING SAFE CLEANUP")
    print("=" * 60)

    freed = 0

    # Delete cache
    cache = OLLAMA / "cache"
    if cache.exists():
        size = get_dir_size(cache)
        shutil.rmtree(cache)
        freed += size
        print(f"[OK] Deleted cache: {size / (1024**2):.1f} MB")

    # Delete history
    history = OLLAMA / "history"
    if history.exists():
        size = get_dir_size(history)
        shutil.rmtree(history)
        freed += size
        print(f"[OK] Deleted history: {size / 1024:.1f} KB")

    # Delete logs
    logs = OLLAMA / "logs"
    if logs.exists():
        size = get_dir_size(logs)
        shutil.rmtree(logs)
        freed += size
        print(f"[OK] Deleted logs: {size / (1024**2):.1f} MB")

    print(f"\nTotal freed: {freed / (1024**2):.1f} MB")
    return freed

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--clean":
        analyze_space()
        safe_cleanup()
    else:
        analyze_space()
        print("\nRun with --clean to perform safe cleanup")
