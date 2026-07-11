"""Distribution module. Posts content to Telegram channel."""
import httpx
from pathlib import Path

HOME = Path("/data/data/com.termux/files/home")
KEYS = HOME / ".quillyos" / "keys"

def load_key(name):
    kf = KEYS / f"{name}.key"
    return kf.read_text().strip() if kf.exists() else None

async def post_to_telegram(message, chat_id="@your_channel_name"):
    """Post message to Telegram channel."""
    token = load_key("telegram")
    if not token:
        print("[!] No Telegram token found")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    async with httpx.AsyncClient() as client:
        r = await client.post(url, json={
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        })
        if r.status_code == 200 and r.json().get("ok"):
            print(f"[+] Posted to Telegram: {r.json()['result']['message_id']}")
            return True
        else:
            print(f"[!] Failed: {r.text[:200]}")
            return False

if __name__ == "__main__":
    import asyncio
    asyncio.run(post_to_telegram("<b>Test post</b> from QuillyOS UGC pipeline!"))
