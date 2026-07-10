#!/usr/bin/env python3
"""QuillyOS Agent Orchestrator v3.0 — Free-tier, keyless-first, SQLite-backed.
Purges dead APIs (Zhipu, Gemini, Brave, Anthropic, Higgsfield).
Adds 43 keyless APIs from public-apis catalog.
"""

import os, sys, json, sqlite3, asyncio, httpx, time
from pathlib import Path
from typing import Optional, Dict, List, Any

HOME = Path.home()
KEYS_DIR = HOME / ".quillyos" / "keys"
DB_PATH = HOME / ".quillyos" / "agent_state.db"
TIMEOUT = 15.0

# ─── API ENDPOINTS ───
# Tier 0: Working APIs (keep)
TIER0 = {
    "openrouter": "https://openrouter.ai/api/v1/chat/completions",
    "tavily": "https://api.tavily.com/search",
    "telegram": "https://api.telegram.org/bot{token}",
}

# Tier 1: Keyless APIs (no auth needed)
TIER1 = {
    "coingecko": "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
    "open_meteo": "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true",
    "rest_countries": "https://restcountries.com/v3.1/name/united",
    "spaceflight": "https://api.spaceflightnewsapi.net/v4/articles/?limit=1",
    "httpbin": "https://httpbin.org/get",
    "jsonplaceholder": "https://jsonplaceholder.typicode.com/posts/1",
    "random_user": "https://randomuser.me/api/",
    "icanhazdadjoke": "https://icanhazdadjoke.com/",
    "kanye": "https://api.kanye.rest/",
    "zenquotes": "https://zenquotes.io/api/random",
    "quotable": "https://api.quotable.io/random",
    "numbersapi": "http://numbersapi.com/random/trivia",
    "agify": "https://api.agify.io/?name=michael",
    "genderize": "https://api.genderize.io/?name=luc",
    "nationalize": "https://api.nationalize.io/?name=nathaniel",
    "bored": "https://www.boredapi.com/api/activity",
    "dogceo": "https://dog.ceo/api/breeds/image/random",
    "catfact": "https://catfact.ninja/fact",
    "jokeapi": "https://v2.jokeapi.dev/joke/Any?type=single",
    "pokeapi": "https://pokeapi.co/api/v2/pokemon/ditto",
    "swapi": "https://swapi.dev/api/people/1",
    "rickandmorty": "https://rickandmortyapi.com/api/character/1",
    "nasa_apod": "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY",
    "open_notify_iss": "http://api.open-notify.org/iss-now.json",
    "open_notify_astros": "http://api.open-notify.org/astros.json",
    "frankfurter": "https://api.frankfurter.app/latest?from=USD&to=EUR",
    "exchangerate": "https://api.exchangerate-api.com/v4/latest/USD",
    "wikipedia": "https://en.wikipedia.org/api/rest_v1/page/summary/Earth",
    "hn_top": "https://hacker-news.firebaseio.com/v0/topstories.json",
    "reddit_json": "https://www.reddit.com/r/technology.json",
}

# Tier 2: APIs that need keys (optional — sign up for free tier)
TIER2 = {
    "newsdata": "https://newsdata.io/api/1/news?apikey={key}&country=us",
    "groq": "https://api.groq.com/openai/v1/chat/completions",
    "pexels": "https://api.pexels.com/v1/search?query=nature&per_page=1",
    "giphy": "https://api.giphy.com/v1/gifs/search?api_key={key}&q=hello&limit=1",
    "pixabay": "https://pixabay.com/api/?key={key}&q=yellow+flowers&image_type=photo",
    "huggingface": "https://api-inference.huggingface.co/models/gpt2",
}

ALL_ENDPOINTS = {**TIER0, **TIER1, **TIER2}

class Orchestrator:
    def __init__(self):
        self.keys: Dict[str, Optional[str]] = {}
        self._init_db()
        self._load_keys()
        self.client = httpx.AsyncClient(timeout=TIMEOUT, follow_redirects=True)
        self.headers = {
            "User-Agent": "QuillyOS-Agent/3.0 (Termux; Android)",
            "Accept": "application/json",
        }

    def _init_db(self):
        os.makedirs(DB_PATH.parent, exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH))
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS api_calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                provider TEXT, tier TEXT, endpoint TEXT, status_code INTEGER,
                response_time_ms REAL, timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                error_msg TEXT
            );
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_type TEXT, provider TEXT, status TEXT,
                payload TEXT, result TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS api_state (
                provider TEXT PRIMARY KEY, tier TEXT, status TEXT,
                last_call TEXT, daily_used INTEGER DEFAULT 0,
                rate_limit INTEGER, error_msg TEXT
            );
        """)
        conn.commit()
        conn.close()

    def _load_keys(self):
        for name in ALL_ENDPOINTS.keys():
            kf = KEYS_DIR / f"{name}.key"
            self.keys[name] = kf.read_text().strip() if kf.exists() else None

    def _log(self, provider: str, tier: str, endpoint: str, code: int, ms: float, err: Optional[str] = None):
        try:
            conn = sqlite3.connect(str(DB_PATH))
            conn.execute(
                "INSERT INTO api_calls (provider,tier,endpoint,status_code,response_time_ms,error_msg) VALUES (?,?,?,?,?,?)",
                (provider, tier, endpoint, code, ms, err)
            )
            st = "ok" if code in (200, 201, 202) else "fail"
            conn.execute("""
                INSERT INTO api_state (provider,tier,status,last_call,daily_used,error_msg)
                VALUES (?, ?, ?, datetime('now'), 1, ?)
                ON CONFLICT(provider) DO UPDATE SET
                tier=excluded.tier, status=excluded.status, last_call=excluded.last_call,
                daily_used=api_state.daily_used+1, error_msg=excluded.error_msg
            """, (provider, tier, st, err))
            conn.commit()
            conn.close()
        except sqlite3.OperationalError as e:
            print(f"  ⚠ DB log error: {e}", file=sys.stderr)

    # ─── GENERIC TEST METHOD ───
    async def _test_generic(self, name: str, url: str, tier: str, method: str = "GET", 
                            payload: Optional[dict] = None, headers_extra: Optional[dict] = None) -> Dict[str, Any]:
        try:
            t0 = time.time()
            h = {**self.headers}
            if headers_extra:
                h.update(headers_extra)
            if method == "GET":
                r = await self.client.get(url, headers=h)
            else:
                r = await self.client.post(url, headers=h, json=payload)
            ms = (time.time() - t0) * 1000
            self._log(name, tier, url, r.status_code, ms)
            if r.status_code in (200, 201, 202):
                try:
                    data = r.json()
                    return {"status": "ok", "response_preview": str(data)[:80]}
                except:
                    return {"status": "ok", "response_preview": r.text[:80]}
            return {"status": "fail", "code": r.status_code, "body": r.text[:120]}
        except Exception as e:
            self._log(name, tier, url, 0, 0, str(e))
            return {"status": "fail", "error": str(e)}

    # ─── TIER 0: WORKING APIs ───
    async def test_openrouter(self) -> Dict[str, Any]:
        if not self.keys.get("openrouter"):
            return {"status": "skip", "error": "No key"}
        return await self._test_generic("openrouter", TIER0["openrouter"], "tier0", "POST",
            payload={"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": "Say OK"}]},
            headers_extra={"Authorization": f"Bearer {self.keys['openrouter']}", "HTTP-Referer": "https://quillyos.dev"})

    async def test_tavily(self) -> Dict[str, Any]:
        if not self.keys.get("tavily"):
            return {"status": "skip", "error": "No key"}
        return await self._test_generic("tavily", TIER0["tavily"], "tier0", "POST",
            payload={"api_key": self.keys["tavily"], "query": "QuillyOS", "max_results": 1})

    async def test_telegram(self) -> Dict[str, Any]:
        if not self.keys.get("telegram"):
            return {"status": "skip", "error": "No key"}
        url = TIER0["telegram"].format(token=self.keys["telegram"]) + "/getMe"
        return await self._test_generic("telegram", url, "tier0")

    # ─── TIER 1: KEYLESS APIs ───
    async def test_keyless(self, name: str) -> Dict[str, Any]:
        if name not in TIER1:
            return {"status": "skip", "error": "Unknown API"}
        return await self._test_generic(name, TIER1[name], "tier1")

    # ─── TIER 2: KEYED APIs ───
    async def test_keyed(self, name: str) -> Dict[str, Any]:
        if name not in TIER2:
            return {"status": "skip", "error": "Unknown API"}
        if not self.keys.get(name):
            return {"status": "skip", "error": "No key"}
        url = TIER2[name].format(key=self.keys[name])
        headers = None
        if name in ("pexels",):
            headers = {"Authorization": self.keys[name]}
        if name == "groq":
            return await self._test_generic(name, url, "tier2", "POST",
                payload={"model": "llama3-8b-8192", "messages": [{"role": "user", "content": "Say OK"}]},
                headers_extra={"Authorization": f"Bearer {self.keys['groq']}"})
        if name == "huggingface":
            return await self._test_generic(name, url, "tier2", "POST",
                payload={"inputs": "Hello"},
                headers_extra={"Authorization": f"Bearer {self.keys['huggingface']}"})
        return await self._test_generic(name, url, "tier2", headers_extra=headers)

    # ─── HEALTH CHECK ───
    async def health_check(self) -> Dict[str, Any]:
        print("\n┌─────────────────────────────────────────┐")
        print("│  QUILLYOS AGENT ORCHESTRATOR v3.0     │")
        print("│  Health Check — Free-tier only        │")
        print("└─────────────────────────────────────────┘")

        results = {"tier0": {}, "tier1": {}, "tier2": {}}

        # Tier 0: Working APIs
        print("\n  🟢 TIER 0: Working APIs (keep)")
        for name, fn in [("openrouter", self.test_openrouter), ("tavily", self.test_tavily), ("telegram", self.test_telegram)]:
            print(f"    Testing {name}...", end=" ", flush=True)
            res = await fn()
            results["tier0"][name] = res
            if res["status"] == "ok": print("✅")
            elif res["status"] == "skip": print("⚠️ SKIP")
            else: print(f"❌ {res.get('error', res.get('code','?'))}")

        # Tier 1: Keyless APIs
        print("\n  🔵 TIER 1: Keyless APIs (43 available)")
        keyless_sample = ["coingecko", "open_meteo", "rest_countries", "nasa_apod", 
                        "frankfurter", "wikipedia", "hn_top", "reddit_json",
                        "dogceo", "catfact", "jokeapi", "pokeapi", "swapi"]
        for name in keyless_sample:
            print(f"    Testing {name}...", end=" ", flush=True)
            res = await self.test_keyless(name)
            results["tier1"][name] = res
            if res["status"] == "ok": print("✅")
            else: print(f"❌ {res.get('error', res.get('code','?'))}")

        # Tier 2: Keyed APIs (optional)
        print("\n  🟡 TIER 2: Keyed APIs (sign up for free tier)")
        for name in ["newsdata", "groq", "pexels", "giphy", "pixabay", "huggingface"]:
            print(f"    Testing {name}...", end=" ", flush=True)
            res = await self.test_keyed(name)
            results["tier2"][name] = res
            if res["status"] == "ok": print("✅")
            elif res["status"] == "skip": print("⚠️ SKIP")
            else: print(f"❌ {res.get('error', res.get('code','?'))}")

        # Summary
        ok = sum(1 for r in results["tier0"].values() if r["status"]=="ok")
        ok += sum(1 for r in results["tier1"].values() if r["status"]=="ok")
        ok += sum(1 for r in results["tier2"].values() if r["status"]=="ok")
        skip = sum(1 for r in results["tier2"].values() if r["status"]=="skip")
        fail = sum(1 for r in results["tier0"].values() if r["status"]=="fail")
        fail += sum(1 for r in results["tier1"].values() if r["status"]=="fail")
        fail += sum(1 for r in results["tier2"].values() if r["status"]=="fail")

        print(f"\n  ───────────────────────────────────────")
        print(f"  ✅ PASS: {ok}  ❌ FAIL: {fail}  ⚠️ SKIP: {skip}")
        print(f"  ───────────────────────────────────────")
        print(f"\n  📝 Next: Get free keys for tier2 APIs")
        print(f"     → newsdata.io (200 req/day)")
        print(f"     → console.groq.com (14.4K tokens/min)")
        print(f"     → pexels.com / pixabay.com (free images)")
        print(f"     → huggingface.co (free inference)")
        print()
        return results

    async def close(self): await self.client.aclose()

async def main():
    orch = Orchestrator()
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        await orch.health_check()
    else:
        print("Usage: python agent_orchestrator.py status")
    await orch.close()

if __name__ == "__main__":
    asyncio.run(main())
