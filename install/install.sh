#!/bin/bash
# QUILLYOS // NEXUS — Clone-to-Node Installer
# One-liner: curl -sL https://raw.githubusercontent.com/q-u-i-l-l-y/quillyos-nexus/main/install/install.sh | bash

set -e

REPO_URL="https://github.com/q-u-i-l-l-y/quillyos-nexus.git"
INSTALL_DIR="$HOME/quillyos/quillyos-nexus"
NODE_ID="node-$(date +%s)-$(hostname | md5sum | head -c 8)"

echo "========================================"
echo "  QUILLYOS // NEXUS"
echo "  Clone-to-Node Protocol v4.0"
echo "========================================"
echo ""

# Detect OS and environment
if [[ "$OSTYPE" == "linux-android"* ]] || [[ -n "$TERMUX_VERSION" ]]; then
    NODE_TYPE="Spoke-Compute"
    PLATFORM="termux"
    echo "[INFO] Detected: Termux (Android)"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if [[ -f /etc/rpi-issue ]] || [[ -f /etc/apt/sources.list.d/raspi.list ]]; then
        NODE_TYPE="Spoke-Compute"
        PLATFORM="raspberry-pi"
        echo "[INFO] Detected: Raspberry Pi"
    else
        NODE_TYPE="Hub"
        PLATFORM="linux-desktop"
        echo "[INFO] Detected: Linux Desktop/Server"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    NODE_TYPE="Hub"
    PLATFORM="macos"
    echo "[INFO] Detected: macOS"
else
    NODE_TYPE="Spoke-Compute"
    PLATFORM="unknown"
    echo "[WARN] Unknown platform — defaulting to Spoke-Compute"
fi

echo "[INFO] Assigned node type: $NODE_TYPE"
echo "[INFO] Generated node ID: $NODE_ID"
echo ""

# Check dependencies
echo "[CHECK] Verifying dependencies..."
MISSING=()

if ! command -v git &> /dev/null; then
    MISSING+=("git")
fi

if ! command -v python3 &> /dev/null; then
    MISSING+=("python3")
fi

if [ ${#MISSING[@]} -ne 0 ]; then
    echo "[WARN] Missing dependencies: ${MISSING[*]}"
    if [[ "$PLATFORM" == "termux" ]]; then
        echo "[INFO] Installing via pkg..."
        pkg update -y
        pkg install -y git python
    elif [[ "$PLATFORM" == "raspberry-pi" ]] || [[ "$PLATFORM" == "linux-desktop" ]]; then
        echo "[INFO] Installing via apt..."
        sudo apt-get update
        sudo apt-get install -y git python3 python3-pip
    elif [[ "$PLATFORM" == "macos" ]]; then
        echo "[INFO] Please install: brew install git python3"
        exit 1
    fi
else
    echo "[OK] All dependencies present"
fi

# Clone repository
echo ""
echo "[CLONE] Pulling quillyos-nexus..."
if [ -d "$INSTALL_DIR" ]; then
    echo "[INFO] Directory exists — updating..."
    cd "$INSTALL_DIR"
    git pull origin main
else
    mkdir -p "$HOME/quillyos"
    git clone "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# Create node self-definition
echo ""
echo "[CONFIG] Creating node identity..."
mkdir -p nodes/self

cat > "nodes/self/$NODE_ID.json" <<EOF
{
  "node_id": "$NODE_ID",
  "node_type": "$NODE_TYPE",
  "platform": "$PLATFORM",
  "registered": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "status": "active",
  "protocol_version": "4.0",
  "capabilities": {
    "git": true,
    "python3": true,
    "layers": [0, 1, 2]
  },
  "context_matrices": [],
  "steward": "self"
}
EOF

echo "[OK] Node identity created: nodes/self/$NODE_ID.json"

# Set up aliases
echo ""
echo "[SETUP] Installing QuillyOS aliases..."

if [[ "$PLATFORM" == "termux" ]]; then
    SHELL_RC="$HOME/.bashrc"
else
    SHELL_RC="$HOME/.bashrc"
    if [ -f "$HOME/.zshrc" ]; then
        SHELL_RC="$HOME/.zshrc"
    fi
fi

# Add quillyos-nexus to PATH and aliases
cat >> "$SHELL_RC" <<'ALIAS_EOF'

# === QUILLYOS NEXUS ALIASES ===
export QUILLYOS_NEXUS="$HOME/quillyos/quillyos-nexus"
alias nexus-pull='cd $QUILLYOS_NEXUS && git pull origin main'
alias nexus-status='cd $QUILLYOS_NEXUS && git status'
alias nexus-commit='cd $QUILLYOS_NEXUS && git add -A && git commit -m'
alias nexus-push='cd $QUILLYOS_NEXUS && git push origin main'
alias nexus-log='cd $QUILLYOS_NEXUS && git log --oneline -10'
# === END QUILLYOS NEXUS ALIASES ===
ALIAS_EOF

echo "[OK] Aliases added to $SHELL_RC"

# Create local context matrix symlinks based on node type
echo ""
echo "[MATRIX] Linking context matrices..."

if [[ "$NODE_TYPE" == "Spoke-Revenue" ]]; then
    ln -sf "../../contexts/matrices/matrix-001.md" "nodes/self/context.md"
    echo "[OK] Linked: matrix-001 (Revenue & Finance)"
elif [[ "$NODE_TYPE" == "Spoke-Health" ]]; then
    ln -sf "../../contexts/matrices/matrix-002.md" "nodes/self/context.md"
    echo "[OK] Linked: matrix-002 (Hardware & ENDS)"
elif [[ "$NODE_TYPE" == "Spoke-Compute" ]]; then
    ln -sf "../../contexts/matrices/matrix-003.md" "nodes/self/context.md"
    echo "[OK] Linked: matrix-003 (Research & Knowledge)"
else
    # Hub gets all matrices
    echo "[OK] Hub node — all matrices accessible"
fi

echo ""
echo "========================================"
echo "  CLONE-TO-NODE COMPLETE"
echo "========================================"
echo ""
echo "Node ID:     $NODE_ID"
echo "Node Type:   $NODE_TYPE"
echo "Platform:    $PLATFORM"
echo "Location:    $INSTALL_DIR"
echo ""
echo "Next steps:"
echo "  1. Source your shell: source $SHELL_RC"
echo "  2. Review your node:   cat nodes/self/$NODE_ID.json"
echo "  3. Read the protocol:  cat protocols/layers/layer-000-observation.md"
echo "  4. Join the mesh:      nexus-push (after committing your node)"
echo ""
echo "You are now a spoke in the QuillyOS mesh."
echo "Protocol version: 4.0"
echo ""
