#!/usr/bin/env python3
"""
Emergency Space Recovery for Termux
Frees disk space WITHOUT deleting backups or downloads
"""

import os
import shutil
import subprocess
from pathlib import Path

HOME = Path.home()
OLLAMA = HOME / ".ollama"

def get_size(path):
    """Get size of file or directory."""
    if path.is_file():
        return path.stat().st_size
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += get_size(Path(entry.path))
    return total

def format_size(size):
    """Format bytes to human readable."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

def main():
    print("=" * 60)
    print("EMERGENCY SPACE RECOVERY")
    print("PRESERVES: backups, downloads, go toolchain")
    print("=" * 60)

    freed = 0

    # 1. Kill Ollama processes
    print("\n[1/8] Killing Ollama processes...")
    subprocess.run(["pkill", "-9", "ollama"], capture_output=True)
    subprocess.run(["pkill", "-9", "llama-server"], capture_output=True)
    print("  [OK] Ollama killed")

    # 2. Delete Ollama cache
    cache = OLLAMA / "cache"
    if cache.exists():
        size = get_size(cache)
        shutil.rmtree(cache)
        freed += size
        print(f"  [OK] Deleted Ollama cache: {format_size(size)}")

    # 3. Delete Ollama history
    history = OLLAMA / "history"
    if history.exists():
        size = get_size(history)
        shutil.rmtree(history)
        freed += size
        print(f"  [OK] Deleted Ollama history: {format_size(size)}")

    # 4. Delete Ollama logs
    logs = OLLAMA / "logs"
    if logs.exists():
        size = get_size(logs)
        shutil.rmtree(logs)
        freed += size
        print(f"  [OK] Deleted Ollama logs: {format_size(size)}")

    # 5. Delete old model manifests (not blobs yet)
    manifests = OLLAMA / "models" / "manifests"
    if manifests.exists():
        # Find old qwen2.5 manifests
        qwen25 = manifests / "registry.ollama.ai" / "library" / "qwen2.5"
        if qwen25.exists():
            size = get_size(qwen25)
            shutil.rmtree(qwen25)
            freed += size
            print(f"  [OK] Deleted Qwen 2.5 manifests: {format_size(size)}")

    # 6. Delete Python cache
    print("\n[6/8] Cleaning Python cache...")
    pycache_count = 0
    for root, dirs, files in os.walk(HOME):
        for d in dirs:
            if d == "__pycache__":
                pycache_path = Path(root) / d
                size = get_size(pycache_path)
                shutil.rmtree(pycache_path)
                freed += size
                pycache_count += 1
    print(f"  [OK] Deleted {pycache_count} __pycache__ dirs")

    # 7. Delete pip cache
    pip_cache = HOME / ".cache" / "pip"
    if pip_cache.exists():
        size = get_size(pip_cache)
        shutil.rmtree(pip_cache)
        freed += size
        print(f"  [OK] Deleted pip cache: {format_size(size)}")

    # 8. Git garbage collection
    print("\n[8/8] Running git garbage collection...")
    nexus = HOME / "quillyos" / "quillyos-nexus"
    if nexus.exists():
        result = subprocess.run(
            ["git", "gc", "--prune=now", "--aggressive"],
            cwd=nexus,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("  [OK] Git GC completed")
        else:
            print(f"  [WARN] Git GC: {result.stderr[:100]}")

    # Summary
    print("\n" + "=" * 60)
    print("RECOVERY SUMMARY")
    print("=" * 60)
    print(f"Total freed: {format_size(freed)}")
    print(f"\nPRESERVED (NOT deleted):")
    print(f"  - ~/picoclaw_project_backup.tar.gz")
    print(f"  - ~/gws.tar.gz")
    print(f"  - ~/downloads/")
    print(f"  - ~/go/")
    print(f"  - ~/.ollama/models/blobs/ (model weights)")
    print(f"\nNext steps:")
    print(f"  1. Check space: df -h")
    print(f"  2. If still full, manually delete old model blobs:")
    print(f"     ollama rm qwen2.5:0.5b")
    print(f"  3. Commit vision metadata to git")
    print(f"  4. Create text-only model")

if __name__ == "__main__":
    main()
