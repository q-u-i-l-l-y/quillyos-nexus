#!/usr/bin/env python3
"""
Qwen 3.5 Vision Component Extractor
Extracts multimodal vision weights for Raspberry Pi 3 deployment
Saves to quillyos-nexus/models/vision/ for later use

Usage:
    python3 extract-vision.py
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime, timezone

HOME = Path.home()
OLLAMA_MODELS = HOME / ".ollama" / "models" / "blobs"
NEXUS = HOME / "quillyos" / "quillyos-nexus"
VISION_DIR = NEXUS / "models" / "vision" / "qwen3.5-0.8b"

def extract_vision_manifest():
    """Extract vision model manifest from Ollama."""
    manifest_dir = HOME / ".ollama" / "models" / "manifests" / "registry.ollama.ai" / "library" / "qwen3.5"

    manifests = list(manifest_dir.glob("*"))
    if not manifests:
        print("[ERR] No Qwen 3.5 manifests found")
        return None

    # Find the 0.8b manifest
    target = None
    for m in manifests:
        if "0.8b" in m.name.lower():
            target = m
            break

    if not target:
        print(f"[ERR] No 0.8b manifest found. Available: {[m.name for m in manifests]}")
        return None

    with open(target) as f:
        manifest = json.load(f)

    return manifest

def extract_vision_weights(manifest):
    """Extract vision-specific blob references."""
    vision_blobs = []

    for layer in manifest.get("layers", []):
        media_type = layer.get("mediaType", "")

        # Vision components are typically identified by:
        # - application/vnd.ollama.image.model (vision encoder)
        # - application/vnd.ollama.image.projector (projection layer)
        if "image" in media_type or "vision" in media_type:
            vision_blobs.append({
                "digest": layer["digest"],
                "size": layer.get("size", 0),
                "type": media_type,
            })
            print(f"  Found vision blob: {layer['digest'][:19]}... ({layer.get('size', 0)} bytes)")

    return vision_blobs

def copy_vision_blobs(vision_blobs):
    """Copy vision blobs to Nexus for safekeeping."""
    VISION_DIR.mkdir(parents=True, exist_ok=True)

    copied = []
    for blob in vision_blobs:
        # Ollama stores blobs as sha256-<hash>
        digest = blob["digest"]
        hash_part = digest.replace("sha256:", "sha256-")
        src = OLLAMA_MODELS / hash_part
        dst = VISION_DIR / hash_part

        if src.exists():
            if not dst.exists():
                shutil.copy2(src, dst)
                print(f"  [OK] Copied {hash_part[:30]}...")
            else:
                print(f"  [SKIP] Already exists: {hash_part[:30]}...")
            copied.append({
                "digest": digest,
                "filename": hash_part,
                "size": blob["size"],
                "type": blob["type"],
            })
        else:
            print(f"  [ERR] Source not found: {src}")

    return copied

def create_vision_metadata(copied_blobs, manifest):
    """Create metadata file for Pi 3 deployment."""
    metadata = {
        "model": "qwen3.5:0.8b",
        "component": "vision_encoder",
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "source_device": "Termux (Android aarch64)",
        "target_device": "Raspberry Pi 3 (armv7l/aarch64)",
        "total_blobs": len(copied_blobs),
        "total_size": sum(b["size"] for b in copied_blobs),
        "blobs": copied_blobs,
        "config": manifest.get("config", {}),
        "notes": [
            "Vision encoder extracted for Raspberry Pi 3 deployment",
            "Text-only model should be created for Termux to save RAM",
            "Re-assemble on Pi 3 using ollama create with Modelfile",
        ],
    }

    meta_file = VISION_DIR / "metadata.json"
    with open(meta_file, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\n[OK] Metadata saved: {meta_file}")
    print(f"[INFO] Total vision component size: {metadata['total_size'] / (1024*1024):.1f} MB")

    return metadata

def create_text_only_modelfile():
    """Create Modelfile for text-only deployment on Termux."""
    modelfile = NEXUS / "models" / "qwen3.5-0.8b-text-only.modelfile"
    modelfile.parent.mkdir(parents=True, exist_ok=True)

    content = """# Qwen 3.5 0.8B Text-Only
# Stripped of vision components for Termux deployment
# Vision components saved in models/vision/ for Pi 3

FROM qwen3.5:0.8b

# Force text-only mode
PARAMETER num_ctx 8192
PARAMETER num_predict 2048
PARAMETER temperature 0.3
PARAMETER top_k 40
PARAMETER top_p 0.9

# System prompt for Revenue Engine
SYSTEM You are the QuillyOS Revenue Engine. Analyze deals, track margins, suggest actions. Output structured JSON with: deal_id, source, margin_percent, risk_level, confidence, recommended_action, timestamp.
"""

    with open(modelfile, "w") as f:
        f.write(content)

    print(f"[OK] Text-only Modelfile: {modelfile}")
    return modelfile

def main():
    print("=" * 50)
    print("Qwen 3.5 Vision Component Extractor")
    print("=" * 50)

    # Step 1: Extract manifest
    print("\n[1/4] Extracting manifest...")
    manifest = extract_vision_manifest()
    if not manifest:
        return 1

    # Step 2: Find vision blobs
    print("\n[2/4] Finding vision components...")
    vision_blobs = extract_vision_weights(manifest)
    if not vision_blobs:
        print("[WARN] No vision-specific blobs found. Model may be text-only already.")
        # Still create metadata and modelfile

    # Step 3: Copy to Nexus
    print("\n[3/4] Copying to Nexus...")
    copied = copy_vision_blobs(vision_blobs)

    # Step 4: Create metadata
    print("\n[4/4] Creating metadata...")
    metadata = create_vision_metadata(copied, manifest)

    # Create text-only Modelfile
    print("\n[5/5] Creating text-only Modelfile...")
    create_text_only_modelfile()

    print("\n" + "=" * 50)
    print("EXTRACTION COMPLETE")
    print("=" * 50)
    print(f"Vision components: {VISION_DIR}")
    print(f"Text-only Modelfile: {NEXUS}/models/qwen3.5-0.8b-text-only.modelfile")
    print(f"\nNext steps:")
    print("  1. Commit vision components to git")
    print("  2. Create text-only model: ollama create qwen3.5-0.8b-text -f models/qwen3.5-0.8b-text-only.modelfile")
    print("  3. Update PicoClaw config to use qwen3.5-0.8b-text")
    print("  4. On Pi 3: Re-assemble full model with vision components")

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
