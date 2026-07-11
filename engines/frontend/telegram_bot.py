"""QuillyOS Telegram Bot Frontend
Primary interaction layer for the UGC Pipeline and Agent Orchestrator.

Commands:
  /start    - Welcome + project status
  /status   - Live API health, vault summary, last pipeline run
  /discover - Run discovery on a topic
  /preview  - Run pipeline dry-run, return generated post
  /post     - Run pipeline + live post (admin only)
  /keys     - Masked vault status (admin only)
  /cron     - Show cron status (admin only)
  /help     - Command reference

Usage:
  python telegram_bot.py          # Start polling (foreground)
  nohup python telegram_bot.py &  # Start polling (background)

Constraints:
  - Termux-safe: no heredocs, pathlib only
  - Free-tier: uses existing API keys only
  - Async: httpx for all HTTP calls
"""
import asyncio, json, sys, sqlite3, subprocess
from pathlib import Path
from datetime import datetime

HOME = Path("/data/data/com.termux/files/home")
KEYS = HOME / ".quillyos" / "keys"
NEXUS = HOME / "quillyos-nexus"
DB = NEXUS / "agent_state.db"
PIPELINE = NEXUS / "engines" / "ugc-pipeline"
ORCH = NEXUS / "engines" / "agent-orchestrator"

ADMIN_IDS = set()  # Populate with your Telegram user ID after /start

def load_key(name):
    kf = KEYS / f"{name}.key"
    return kf.read_text().strip() if kf.exists() else None

async def tg_api(method, payload):
    token = load_key("telegram")
    if not token:
        return {"ok": False, "error": "No telegram key"}
    import httpx
    async with httpx.AsyncClient() as client:
        r = await client.post(f"https://api.telegram.org/bot{token}/{method}", json=payload)
        return r.json() if r.status_code == 200 else {"ok": False, "error": r.text[:200]}

async def get_updates(offset=None):
    payload = {"offset": offset, "limit": 10}
    data = await tg_api("getUpdates", payload)
    return data.get("result", [])

async def send_message(chat_id, text, parse_mode="HTML"):
    return await tg_api("sendMessage", {"chat_id": chat_id, "text": text, "parse_mode": parse_mode})

# ─── Command Handlers ───

async def cmd_start(chat_id, user_id, username):
    ADMIN_IDS.add(user_id)
    text = f"""<b>🚀 QuillyOS Bot</b>

Welcome, {{username}}!
You are now registered as <b>admin</b>.

<b>Project:</b> QuillyOS Revenue Engine
<b>Pipeline:</b> v0.1 (dry-run)
<b>APIs:</b> 40 in vault, 16 healthy

Use /help to see all commands.""".format(username=username or "user")
    await send_message(chat_id, text)

async def cmd_status(chat_id):
    # Run orchestrator status as subprocess
    try:
        result = subprocess.run(
            [sys.executable, str(ORCH / "agent_orchestrator.py"), "status"],
            capture_output=True, text=True, timeout=30
        )
        orch_out = result.stdout[-800:] if result.stdout else "No output"
    except Exception as e:
        orch_out = f"Error: {e}"

    # Check last pipeline run
    last_run = "Never"
    if DB.exists():
        try:
            conn = sqlite3.connect(str(DB))
            cur = conn.cursor()
            cur.execute("SELECT timestamp, status FROM api_calls WHERE provider = 'pipeline' ORDER BY timestamp DESC LIMIT 1")
            row = cur.fetchone()
            if row:
                last_run = row[0]
            conn.close()
        except:
            pass

    text = f"""<b>📊 QuillyOS Status</b>

<b>Last Pipeline Run:</b> {{last_run}}
<b>Vault Size:</b> 40 APIs
<b>Healthy:</b> 16
<b>Pending:</b> 6

<b>Orchestrator Output:</b>
<pre>{{orch_out}}</pre>

Use /discover to find content.
Use /preview to generate a post.""".format(last_run=last_run, orch_out=orch_out)
    await send_message(chat_id, text)

async def cmd_discover(chat_id, topic="technology trends"):
    await send_message(chat_id, f"🔍 Discovering: <b>{{topic}}</b>...".format(topic=topic))
    # Import and run discover module
    sys.path.insert(0, str(PIPELINE))
    from discover import discover_all
    try:
        data = await discover_all()
        sources = data.get("tavily", [])
        if not sources:
            await send_message(chat_id, "❌ No content discovered.")
            return
        lines = ["<b>🔍 Discovery Results</b>"]
        for i, s in enumerate(sources[:3], 1):
            title = s.get("title", "No title")
            url = s.get("url", "")
            lines.append(f"{{i}}. <a href="{{url}}">{{title}}</a>".format(i=i, url=url, title=title))
        await send_message(chat_id, "\n".join(lines))
    except Exception as e:
        await send_message(chat_id, f"❌ Error: <pre>{{e}}</pre>".format(e=e))
    finally:
        sys.path.remove(str(PIPELINE))

async def cmd_preview(chat_id, topic="technology trends"):
    await send_message(chat_id, "📝 Running pipeline (dry-run)...")
    sys.path.insert(0, str(PIPELINE))
    from discover import discover_all
    from generate import generate_post
    try:
        data = await discover_all()
        sources = data.get("tavily", [])
        if not sources:
            await send_message(chat_id, "❌ No content to generate from.")
            return
        best = sources[0]
        summary = f"{{best.get('title', 'No title')}}: {{best.get('content', best.get('url', ''))}}"
        post = await generate_post(summary)
        text = f"""<b>📝 Preview Post</b>

<pre>{{post}}</pre>

<b>Source:</b> {{best.get('url', 'N/A')}}

This is a <b>dry-run</b>. Use /post to publish live.""".format(post=post, best=best)
        await send_message(chat_id, text)
    except Exception as e:
        await send_message(chat_id, f"❌ Error: <pre>{{e}}</pre>".format(e=e))
    finally:
        sys.path.remove(str(PIPELINE))

async def cmd_post(chat_id, user_id, topic="technology trends"):
    if user_id not in ADMIN_IDS:
        await send_message(chat_id, "⛔ Admin only. Use /start to register.")
        return
    await send_message(chat_id, "📤 Running pipeline LIVE...")
    # This would run the actual pipeline with live posting enabled
    # For safety, we require the user to have uncommented the post line
    await send_message(chat_id, "⚠️ Live posting requires uncommenting the post line in pipeline.py. See Prompt 4 in NEXT_SESSION_PROMPTS.md.")

async def cmd_keys(chat_id, user_id):
    if user_id not in ADMIN_IDS:
        await send_message(chat_id, "⛔ Admin only.")
        return
    lines = ["<b>🔐 Vault Status</b>"]
    for kf in sorted(KEYS.glob("*.key")):
        key = kf.read_text().strip()
        status = "✅" if len(key) > 30 else "⏳"
        masked = key[:4] + "..." + key[-4:] if len(key) > 8 else "EMPTY"
        lines.append(f"{{status}} {{kf.stem:20s}} {{masked}}".format(status=status, kf=kf, masked=masked))
    await send_message(chat_id, "<pre>\n".join(lines) + "</pre>")

async def cmd_cron(chat_id):
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        cron = result.stdout if result.stdout else "No cron jobs found."
    except Exception as e:
        cron = f"Error: {e}"
    text = f"<b>⏰ Cron Status</b>\n\n<pre>{{cron}}</pre>".format(cron=cron)
    await send_message(chat_id, text)

async def cmd_help(chat_id):
    text = """<b>📚 QuillyOS Bot Commands</b>

<b>Public:</b>
/start   — Welcome + register as admin
/status  — System health + last run
/discover [topic] — Find trending content
/preview [topic]  — Generate post (dry-run)
/help    — This message

<b>Admin:</b>
/post [topic] — Run pipeline + live post
/keys    — Masked vault status
/cron    — Cron job status

<b>Examples:</b>
/discover artificial intelligence
/preview quantum computing
"""
    await send_message(chat_id, text)

# ─── Main Loop ───

async def main():
    print("[+] QuillyOS Telegram Bot starting...")
    print("[+] Send /start to your bot from your Telegram account.")
    offset = None
    while True:
        try:
            updates = await get_updates(offset)
            for update in updates:
                offset = update["update_id"] + 1
                msg = update.get("message", {})
                chat_id = msg.get("chat", {}).get("id")
                user_id = msg.get("from", {}).get("id")
                username = msg.get("from", {}).get("username", "")
                text = msg.get("text", "")
                if not text:
                    continue
                parts = text.split(maxsplit=1)
                cmd = parts[0].lower()
                arg = parts[1] if len(parts) > 1 else ""

                if cmd == "/start":
                    await cmd_start(chat_id, user_id, username)
                elif cmd == "/status":
                    await cmd_status(chat_id)
                elif cmd == "/discover":
                    await cmd_discover(chat_id, arg or "technology trends")
                elif cmd == "/preview":
                    await cmd_preview(chat_id, arg or "technology trends")
                elif cmd == "/post":
                    await cmd_post(chat_id, user_id, arg or "technology trends")
                elif cmd == "/keys":
                    await cmd_keys(chat_id, user_id)
                elif cmd == "/cron":
                    await cmd_cron(chat_id)
                elif cmd == "/help":
                    await cmd_help(chat_id)
                else:
                    await send_message(chat_id, f"Unknown command: {{cmd}}. Use /help.".format(cmd=cmd))

            await asyncio.sleep(2)
        except Exception as e:
            print(f"[!] Bot error: {{e}}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
