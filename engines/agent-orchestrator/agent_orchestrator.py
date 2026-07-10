#!/usr/bin/env python3
"""QuillyOS Agent Orchestrator v2.0 — Coordinates all API utilities.
Termux-compatible, async, SQLite-backed, free-tier only."""

import os, sys, json, sqlite3, asyncio, httpx
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any

# ─── CONFIG ───
HOME = Path.home()
KEYS_DIR = HOME / ".quillyos" / "keys"
DB_PATH = HOME / ".quillyos" / "agent_state.db"
TIMEOUT = 30.0

ENDPOINTS = {
    "zhipu": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
    "gemini": "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
    "openrouter": "https://openrouter.ai/api/v1/chat/completions",
    "tavily": "https://api.tavily.com/search",
    "brave": "https://api.search.brave.com/res/v1/web/search",
    "telegram": "https://api.telegram.org/bot{token}",
    "anthropic": "https://api.anthropic.com/v1/messages",
    "higgsfield": "https://api.higgsfield.ai/v1/generate",
}

class Orchestrator:
    def __init__(self):
        self.keys: Dict[str, Optional[str]] = {}
        self._init_db()
        self._load_keys()
        self.client = httpx.AsyncClient(timeout=TIMEOUT)

    def _init_db(self):
        os.makedirs(DB_PATH.parent, exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH))
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS api_calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                provider TEXT, endpoint TEXT, status_code INTEGER,
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
                provider TEXT PRIMARY KEY, status TEXT,
                last_call TEXT, daily_used INTEGER DEFAULT 0,
                rate_limit INTEGER, error_msg TEXT
            );
        """)
        conn.commit()
        conn.close()

    def _load_keys(self):
        for name in ENDPOINTS.keys():
            kf = KEYS_DIR / f"{name}.key"
            self.keys[name] = kf.read_text().strip() if kf.exists() else None

    def _log(self, provider: str, endpoint: str, code: int, ms: float, err: Optional[str] = None):
        conn = sqlite3.connect(str(DB_PATH))
        conn.execute(
            "INSERT INTO api_calls (provider,endpoint,status_code,response_time_ms,error_msg) VALUES (?,?,?,?,?)",
            (provider, endpoint, code, ms, err)
        )
        st = "ok" if code == 200 else "fail"
        conn.execute("""
            INSERT INTO api_state (provider,status,last_call,daily_used,error_msg)
            VALUES (?, ?, datetime('now'), 1, ?)
            ON CONFLICT(provider) DO UPDATE SET
            status=excluded.status, last_call=excluded.last_call,
            daily_used=api_state.daily_used+1, error_msg=excluded.error_msg
        """, (provider, st, err))
        conn.commit(); conn.close()

    # ─── API TESTS ───
    async def test_zhipu(self) -> Dict[str, Any]:
        if not self.keys.get("zhipu"): return {"status":"fail","error":"No key"}
        try:
            t0 = datetime.now()
            r = await self.client.post(ENDPOINTS["zhipu"],
                headers={"Authorization":f"Bearer {self.keys['zhipu']}"},
                json={"model":"glm-4","messages":[{"role":"user","content":"Say OK"}]})
            ms = (datetime.now()-t0).total_seconds()*1000
            self._log("zhipu", ENDPOINTS["zhipu"], r.status_code, ms)
            if r.status_code == 200:
                return {"status":"ok","response":r.json()["choices"][0]["message"]["content"]}
            return {"status":"fail","code":r.status_code,"body":r.text[:200]}
        except Exception as e:
            self._log("zhipu", ENDPOINTS["zhipu"], 0, 0, str(e)); return {"status":"fail","error":str(e)}

    async def test_gemini(self) -> Dict[str, Any]:
        if not self.keys.get("gemini"): return {"status":"fail","error":"No key"}
        try:
            t0 = datetime.now()
            url = f"{ENDPOINTS['gemini']}?key={self.keys['gemini']}"
            r = await self.client.post(url, json={"contents":[{"parts":[{"text":"Say OK"}]}]})
            ms = (datetime.now()-t0).total_seconds()*1000
            self._log("gemini", ENDPOINTS["gemini"], r.status_code, ms)
            if r.status_code == 200:
                return {"status":"ok","response":r.json()["candidates"][0]["content"]["parts"][0]["text"]}
            return {"status":"fail","code":r.status_code,"body":r.text[:200]}
        except Exception as e:
            self._log("gemini", ENDPOINTS["gemini"], 0, 0, str(e)); return {"status":"fail","error":str(e)}

    async def test_openrouter(self) -> Dict[str, Any]:
        if not self.keys.get("openrouter"): return {"status":"fail","error":"No key"}
        try:
            t0 = datetime.now()
            r = await self.client.post(ENDPOINTS["openrouter"],
                headers={"Authorization":f"Bearer {self.keys['openrouter']}","HTTP-Referer":"https://quillyos.dev","X-Title":"QuillyOS"},
                json={"model":"openai/gpt-3.5-turbo","messages":[{"role":"user","content":"Say OK"}]})
            ms = (datetime.now()-t0).total_seconds()*1000
            self._log("openrouter", ENDPOINTS["openrouter"], r.status_code, ms)
            if r.status_code == 200:
                return {"status":"ok","response":r.json()["choices"][0]["message"]["content"]}
            return {"status":"fail","code":r.status_code,"body":r.text[:200]}
        except Exception as e:
            self._log("openrouter", ENDPOINTS["openrouter"], 0, 0, str(e)); return {"status":"fail","error":str(e)}

    async def test_tavily(self) -> Dict[str, Any]:
        if not self.keys.get("tavily"): return {"status":"fail","error":"No key"}
        try:
            t0 = datetime.now()
            r = await self.client.post(ENDPOINTS["tavily"],
                json={"api_key":self.keys["tavily"],"query":"QuillyOS","max_results":1})
            ms = (datetime.now()-t0).total_seconds()*1000
            self._log("tavily", ENDPOINTS["tavily"], r.status_code, ms)
            if r.status_code == 200:
                return {"status":"ok","results":len(r.json().get("results",[]))}
            return {"status":"fail","code":r.status_code,"body":r.text[:200]}
        except Exception as e:
            self._log("tavily", ENDPOINTS["tavily"], 0, 0, str(e)); return {"status":"fail","error":str(e)}

    async def test_brave(self) -> Dict[str, Any]:
        if not self.keys.get("brave"): return {"status":"fail","error":"No key"}
        try:
            t0 = datetime.now()
            r = await self.client.get(ENDPOINTS["brave"],
                headers={"X-Subscription-Key":self.keys["brave"]},
                params={"q":"QuillyOS","count":1})
            ms = (datetime.now()-t0).total_seconds()*1000
            self._log("brave", ENDPOINTS["brave"], r.status_code, ms)
            if r.status_code == 200:
                return {"status":"ok","results":len(r.json().get("web",{}).get("results",[]))}
            return {"status":"fail","code":r.status_code,"body":r.text[:200]}
        except Exception as e:
            self._log("brave", ENDPOINTS["brave"], 0, 0, str(e)); return {"status":"fail","error":str(e)}

    async def test_telegram(self) -> Dict[str, Any]:
        if not self.keys.get("telegram"): return {"status":"fail","error":"No key"}
        try:
            t0 = datetime.now()
            url = ENDPOINTS["telegram"].format(token=self.keys["telegram"]) + "/getMe"
            r = await self.client.get(url)
            ms = (datetime.now()-t0).total_seconds()*1000
            self._log("telegram", url, r.status_code, ms)
            if r.status_code == 200 and r.json().get("ok"):
                return {"status":"ok","bot":r.json()["result"].get("username","?")}
            return {"status":"fail","code":r.status_code,"body":r.text[:200]}
        except Exception as e:
            self._log("telegram", ENDPOINTS["telegram"], 0, 0, str(e)); return {"status":"fail","error":str(e)}

    async def test_anthropic(self) -> Dict[str, Any]:
        if not self.keys.get("anthropic"): return {"status":"fail","error":"No key"}
        try:
            t0 = datetime.now()
            r = await self.client.post(ENDPOINTS["anthropic"],
                headers={"x-api-key":self.keys["anthropic"],"anthropic-version":"2023-06-01","Content-Type":"application/json"},
                json={"model":"claude-3-haiku-20240307","max_tokens":10,"messages":[{"role":"user","content":"Say OK"}]})
            ms = (datetime.now()-t0).total_seconds()*1000
            self._log("anthropic", ENDPOINTS["anthropic"], r.status_code, ms)
            if r.status_code == 200:
                return {"status":"ok","response":r.json()["content"][0]["text"]}
            return {"status":"fail","code":r.status_code,"body":r.text[:200]}
        except Exception as e:
            self._log("anthropic", ENDPOINTS["anthropic"], 0, 0, str(e)); return {"status":"fail","error":str(e)}

    async def test_higgsfield(self) -> Dict[str, Any]:
        if not self.keys.get("higgsfield"): return {"status":"fail","error":"No key"}
        return {"status":"unknown","note":"Higgsfield endpoint stub — verify at docs.higgsfield.ai"}

    # ─── ORCHESTRATION ───
    async def health_check(self) -> Dict[str, Any]:
        print("\n┌─────────────────────────────────────────┐")
        print("│  QUILLYOS AGENT ORCHESTRATOR v2.0       │")
        print("│  Health Check — Testing all APIs...     │")
        print("└─────────────────────────────────────────┘")
        tests = {
            "zhipu": self.test_zhipu, "gemini": self.test_gemini,
            "openrouter": self.test_openrouter, "tavily": self.test_tavily,
            "brave": self.test_brave, "telegram": self.test_telegram,
            "anthropic": self.test_anthropic, "higgsfield": self.test_higgsfield,
        }
        results = {}
        for name, fn in tests.items():
            print(f"\n  Testing {name}...", end=" ", flush=True)
            res = await fn(); results[name] = res
            if res["status"] == "ok": print("✅ PASS")
            elif res["status"] == "unknown": print("⚠️  SKIP")
            else: print(f"❌ FAIL — {res.get('error', res.get('code','?'))}")
        ok = sum(1 for r in results.values() if r["status"]=="ok")
        fail = sum(1 for r in results.values() if r["status"]=="fail")
        skip = sum(1 for r in results.values() if r["status"]=="unknown")
        print(f"\n  ───────────────────────────────────────")
        print(f"  ✅ PASS: {ok}  ❌ FAIL: {fail}  ⚠️ SKIP: {skip}")
        print(f"  ───────────────────────────────────────\n")
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
