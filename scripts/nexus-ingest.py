#!/usr/bin/env python3
"""
NEXUS INGESTOR v4.0
Wraps document_ingestor_v2.1 with Nexus Protocol classification.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

HOME = Path.home()
NEXUS = HOME / "quillyos" / "quillyos-nexus"

# Try to find existing ingestor
INGESTOR_V21 = None
for path in [
    HOME / ".picoclaw" / "workspace" / "document_ingestor_v2.1.py",
    HOME / "picoclaw-dev" / "document_ingestor_v2.1.py",
    HOME / "document_ingestor_v2.1.py",
]:
    if path.exists():
        INGESTOR_V21 = path
        break

def classify_for_nexus(path, content_sample=""):
    """Classify files into Nexus categories."""
    name = path.name.lower()
    spath = str(path).lower()
    
    # Personal
    for pat in ["*.jpg","*.jpeg","*.png","*.gif","*.mp4","*.mp3","*.pdf","*personal*","*private*","*photo*","*music*","*video*"]:
        if name.endswith(pat.replace("*","")) or pat.replace("*","") in spath:
            return "personal", f"pattern: {pat}"
    
    # Legacy
    for kw in ["phone_bootstrap","legacy","deprecated","superseded","archive","backup","old_"]:
        if kw in name or kw in spath:
            return "archive", f"legacy: {kw}"
    
    # Nexus keywords
    nexus_kw = ["quillyos","nexus","picoclaw","protocol","matrix","entity","observation","evidence","context","consensus","revenue","arbitrage","wholesale","ENDS","metamaterial","quantum","biotech","health","sensor","bootstrap","vision","mission","doctrine","knowledge","superposition","mesh","node","spoke","hub","skill","manifest","automation","workflow"]
    for kw in nexus_kw:
        if kw in name or kw in spath:
            return "commit_to_nexus", f"keyword: {kw}"
    
    matches = [kw for kw in nexus_kw if kw in content_sample.lower()]
    if len(matches) >= 3:
        return "commit_to_nexus", f"content: {', '.join(matches[:3])}"
    if len(matches) >= 1:
        return "merge_required", f"partial: {', '.join(matches[:2])}"
    
    if "quillyos" in spath and name.endswith((".py",".sh",".json",".md")):
        return "commit_to_nexus", "quillyos code"
    
    return "unknown", "no signals"

def scan_device():
    """Scan device and classify all relevant files."""
    print("NEXUS INGESTOR v4.0")
    print("=" * 50)
    
    results = {"commit_to_nexus": [], "merge_required": [], "archive": [], "personal": [], "unknown": []}
    total = 0
    
    for root_path, label in [
        (HOME, "Termux Home"),
        (HOME / "quillyos", "QuillyOS"),
        (Path("/storage/emulated/0/Documents"), "Documents"),
        (Path("/storage/emulated/0/Download"), "Downloads"),
    ]:
        if not root_path.exists():
            print(f"[SKIP] {label}: not accessible")
            continue
        
        print(f"\n[SCAN] {label}: {root_path}")
        count = 0
        
        for path in root_path.rglob("*"):
            if path.is_dir():
                continue
            if path.name.startswith(".") or "__pycache__" in str(path):
                continue
            
            count += 1
            content = ""
            try:
                if path.stat().st_size < 10 * 1024 * 1024:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(4096)
            except:
                pass
            
            cat, reason = classify_for_nexus(path, content)
            results[cat].append({"path": str(path), "relative": str(path.relative_to(root_path)), "size": path.stat().st_size, "reason": reason})
        
        print(f"  Found {count} files")
        total += count
    
    # Report
    print(f"\n{'='*50}")
    print("CLASSIFICATION REPORT")
    print(f"{'='*50}")
    
    for cat, items in results.items():
        if items:
            print(f"\n{cat.upper()}: {len(items)} files")
            for i in items[:5]:
                print(f"  • {i['relative']} ({i['reason']})")
            if len(items) > 5:
                print(f"  ... and {len(items)-5} more")
    
    # Save report
    report_path = HOME / "quillyos" / "ingest-report.json"
    with open(report_path, 'w') as f:
        json.dump({"timestamp": __import__('datetime').datetime.utcnow().isoformat()+"Z", "results": results}, f, indent=2)
    print(f"\nReport saved: {report_path}")
    
    # Show next actions
    print(f"\n{'='*50}")
    print("NEXT ACTIONS")
    print(f"{'='*50}")
    if results["commit_to_nexus"]:
        print(f"→ Stage {len(results['commit_to_nexus'])} files for nexus commit")
    if results["merge_required"]:
        print(f"→ Review {len(results['merge_required'])} files for merge")
    if results["archive"]:
        print(f"→ Archive {len(results['archive'])} legacy files")
    if results["unknown"]:
        print(f"→ Re-run with --interactive to classify {len(results['unknown'])} unknown files")
    
    return results

if __name__ == "__main__":
    try:
        scan_device()
    except KeyboardInterrupt:
        print("\n[INGESTOR] Interrupted.")
