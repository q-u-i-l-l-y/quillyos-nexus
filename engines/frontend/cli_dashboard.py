#!/usr/bin/env python3
"""QuillyOS CLI Dashboard
Run: python cli_dashboard.py
Or alias: echo 'alias qd="python3 ~/quillyos-nexus/engines/frontend/cli_dashboard.py"' >> ~/.bashrc
"""
import subprocess, sys, sqlite3
from pathlib import Path
from datetime import datetime

HOME = Path("/data/data/com.termux/files/home")
NEXUS = HOME / "quillyos-nexus"
KEYS = HOME / ".quillyos" / "keys"
DB = NEXUS / "agent_state.db"

def box(title, lines):
    width = max(len(title), max((len(l) for l in lines), default=0)) + 4
    print("╔" + "═" * width + "╗")
    print("║ " + title.center(width - 2) + " ║")
    print("╠" + "═" * width + "╣")
    for line in lines:
        print("║ " + line.ljust(width - 2) + " ║")
    print("╚" + "═" * width + "╝")

def get_vault_status():
    total = len(list(KEYS.glob("*.key")))
    working = 0
    pending = 0
    for kf in KEYS.glob("*.key"):
        content = kf.read_text().strip()
        if len(content) > 30:
            working += 1
        elif len(content) < 30 and len(content) > 5:
            pending += 1
    return total, working, pending

def get_last_pipeline_run():
    if not DB.exists():
        return "Never"
    try:
        conn = sqlite3.connect(str(DB))
        cur = conn.cursor()
        cur.execute("SELECT timestamp FROM api_calls WHERE provider = 'pipeline' ORDER BY timestamp DESC LIMIT 1")
        row = cur.fetchone()
        conn.close()
        return row[0] if row else "Never"
    except:
        return "Unknown"

def get_cron_status():
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        return "Active" if "ugc-pipeline" in result.stdout else "Inactive"
    except:
        return "Unavailable"

def main():
    total, working, pending = get_vault_status()
    last_run = get_last_pipeline_run()
    cron = get_cron_status()

    box("QUILLYOS CLI DASHBOARD", [
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"Vault:     {total} APIs  ({working} working, {pending} pending)",
        f"Pipeline:  v0.1 (dry-run)",
        f"Last Run:  {last_run}",
        f"Cron:      {cron}",
        "",
        "Commands:",
        "  /discover [topic]  — Find content",
        "  /preview [topic]   — Generate post",
        "  /post [topic]      — Live post",
        "  /keys              — Vault status",
        "  /cron              — Cron status",
    ])

if __name__ == "__main__":
    main()
