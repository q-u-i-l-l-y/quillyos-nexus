#!/usr/bin/env python3
"""QuillyOS Agent Orchestrator — Coordinates all API utilities"""
import os, json, sqlite3, asyncio, httpx
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional, Dict, List, Any

# ─── CONFIG ────────────────────────────────────────────────────────
KEYS_DIR = Path.home() / ".quillyos" / "keys"
DB_PATH = Path.home() / ".quillyos" / "agent_state.db"

class SecureKeyVault:
    """Loads keys from individual files (never in env)"""
    @staticmethod
    def load(provider: str) -> Optional[str]:
        key_file = KEYS_DIR / f"{provider}.key"
        if key_file.exists():
            return key_file.read_text().strip()
        return None

@dataclass
class AgentTask:
    id: int
    task_type: str  # "content", "research", "distribution", "analysis"
    provider_chain: List[str]  # ["zhipu", "openrouter", "telegram"]
    prompt: str
    status: str = "pending"
    result: Any = None
    created_at: str = ""
    completed_at: Optional[str] = None

class AgentOrchestrator:
    """Coordinates multi-API agent workflows"""
    
    def __init__(self):
        self.conn = sqlite3.connect(str(DB_PATH))
        self._init_db()
        self.client = httpx.AsyncClient(timeout=60)
    
    def _init_db(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                task_type TEXT,
                provider_chain TEXT,
                prompt TEXT,
                status TEXT DEFAULT 'pending',
                result TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                completed_at TEXT
            );
            CREATE TABLE IF NOT EXISTS api_calls (
                id INTEGER PRIMARY KEY,
                provider TEXT,
                endpoint TEXT,
                status_code INTEGER,
                latency_ms REAL,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            );
        """)
        self.conn.commit()
    
    async def call_zhipu(self, prompt: str) -> Optional[str]:
        """Zhipu AI — Chinese LLM for content generation"""
        key = SecureKeyVault.load("zhipu")
        if not key:
            return None
        
        url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        payload = {
            "model": "glm-4-flash",
            "messages": [{"role": "user", "content": prompt}]
        }
        
        start = datetime.now()
        try:
            r = await self.client.post(url, headers=headers, json=payload)
            latency = (datetime.now() - start).total_seconds() * 1000
            self.conn.execute("INSERT INTO api_calls (provider, endpoint, status_code, latency_ms) VALUES (?, ?, ?, ?)",
                            ("zhipu", url, r.status_code, latency))
            self.conn.commit()
            
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Zhipu error: {e}")
        return None
    
    async def call_gemini(self, prompt: str) -> Optional[str]:
        """Google Gemini — high-quota fallback"""
        key = SecureKeyVault.load("gemini")
        if not key:
            return None
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        start = datetime.now()
        try:
            r = await self.client.post(url, json=payload)
            latency = (datetime.now() - start).total_seconds() * 1000
            self.conn.execute("INSERT INTO api_calls (provider, endpoint, status_code, latency_ms) VALUES (?, ?, ?, ?)",
                            ("gemini", url, r.status_code, latency))
            self.conn.commit()
            
            if r.status_code == 200:
                return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"Gemini error: {e}")
        return None
    
    async def call_openrouter(self, prompt: str, model: str = "openrouter/free") -> Optional[str]:
        """OpenRouter — model aggregation with free tier"""
        key = SecureKeyVault.load("openrouter")
        if not key:
            return None
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {key}",
            "HTTP-Referer": "https://quillyos.dev",
            "X-Title": "QuillyOS Agent"
        }
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        start = datetime.now()
        try:
            r = await self.client.post(url, headers=headers, json=payload)
            latency = (datetime.now() - start).total_seconds() * 1000
            self.conn.execute("INSERT INTO api_calls (provider, endpoint, status_code, latency_ms) VALUES (?, ?, ?, ?)",
                            ("openrouter", url, r.status_code, latency))
            self.conn.commit()
            
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"OpenRouter error: {e}")
        return None
    
    async def call_tavily(self, query: str) -> Optional[Dict]:
        """Tavily — AI search for research tasks"""
        key = SecureKeyVault.load("tavily")
        if not key:
            return None
        
        url = "https://api.tavily.com/search"
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        payload = {"query": query, "search_depth": "advanced", "max_results": 5}
        
        start = datetime.now()
        try:
            r = await self.client.post(url, headers=headers, json=payload)
            latency = (datetime.now() - start).total_seconds() * 1000
            self.conn.execute("INSERT INTO api_calls (provider, endpoint, status_code, latency_ms) VALUES (?, ?, ?, ?)",
                            ("tavily", url, r.status_code, latency))
            self.conn.commit()
            
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"Tavily error: {e}")
        return None
    
    async def call_brave(self, query: str) -> Optional[Dict]:
        """Brave Search — privacy-focused web search"""
        key = SecureKeyVault.load("brave")
        if not key:
            return None
        
        url = f"https://api.search.brave.com/res/v1/web/search?q={query}&count=5"
        headers = {"X-Subscription-Token": key, "Accept": "application/json"}
        
        start = datetime.now()
        try:
            r = await self.client.get(url, headers=headers)
            latency = (datetime.now() - start).total_seconds() * 1000
            self.conn.execute("INSERT INTO api_calls (provider, endpoint, status_code, latency_ms) VALUES (?, ?, ?, ?)",
                            ("brave", url, r.status_code, latency))
            self.conn.commit()
            
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"Brave error: {e}")
        return None
    
    async def call_telegram(self, message: str, chat_id: str = "@your_channel") -> bool:
        """Telegram Bot — distribution channel"""
        key = SecureKeyVault.load("telegram")
        if not key:
            return False
        
        url = f"https://api.telegram.org/bot{key}/sendMessage"
        payload = {"chat_id": chat_id, "text": message[:4096], "parse_mode": "HTML"}
        
        start = datetime.now()
        try:
            r = await self.client.post(url, json=payload)
            latency = (datetime.now() - start).total_seconds() * 1000
            self.conn.execute("INSERT INTO api_calls (provider, endpoint, status_code, latency_ms) VALUES (?, ?, ?, ?)",
                            ("telegram", url, r.status_code, latency))
            self.conn.commit()
            return r.json().get("ok", False)
        except Exception as e:
            print(f"Telegram error: {e}")
        return False
    
    async def call_anthropic(self, prompt: str) -> Optional[str]:
        """Anthropic Claude — high-quality reasoning"""
        key = SecureKeyVault.load("anthropic")
        if not key:
            return None
        
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        start = datetime.now()
        try:
            r = await self.client.post(url, headers=headers, json=payload)
            latency = (datetime.now() - start).total_seconds() * 1000
            self.conn.execute("INSERT INTO api_calls (provider, endpoint, status_code, latency_ms) VALUES (?, ?, ?, ?)",
                            ("anthropic", url, r.status_code, latency))
            self.conn.commit()
            
            if r.status_code == 200:
                return r.json()["content"][0]["text"]
        except Exception as e:
            print(f"Anthropic error: {e}")
        return None
    
    async def call_higgsfield(self, prompt: str, image_url: str = None) -> Optional[str]:
        """Higgsfield — video/image generation"""
        api_key = SecureKeyVault.load("higgsfield")
        secret = SecureKeyVault.load("higgsfield_secret")
        if not api_key or not secret:
            return None
        
        # Higgsfield API endpoint for video generation
        url = "https://api.higgsfield.ai/v1/generations"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "X-API-Secret": secret,
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": prompt,
            "type": "video",
            "duration": 5
        }
        if image_url:
            payload["image_url"] = image_url
        
        start = datetime.now()
        try:
            r = await self.client.post(url, headers=headers, json=payload)
            latency = (datetime.now() - start).total_seconds() * 1000
            self.conn.execute("INSERT INTO api_calls (provider, endpoint, status_code, latency_ms) VALUES (?, ?, ?, ?)",
                            ("higgsfield", url, r.status_code, latency))
            self.conn.commit()
            
            if r.status_code == 200:
                return r.json().get("generation_id")
        except Exception as e:
            print(f"Higgsfield error: {e}")
        return None
    
    async def execute_task(self, task: AgentTask) -> AgentTask:
        """Execute a task through its provider chain"""
        print(f"Executing task {task.id}: {task.task_type}")
        
        result = None
        for provider in task.provider_chain:
            print(f"  -> Calling {provider}...")
            
            if provider == "zhipu":
                result = await self.call_zhipu(task.prompt)
            elif provider == "gemini":
                result = await self.call_gemini(task.prompt)
            elif provider == "openrouter":
                result = await self.call_openrouter(task.prompt)
            elif provider == "tavily":
                result = await self.call_tavily(task.prompt)
            elif provider == "brave":
                result = await self.call_brave(task.prompt)
            elif provider == "telegram":
                result = await self.call_telegram(task.prompt)
            elif provider == "anthropic":
                result = await self.call_anthropic(task.prompt)
            elif provider == "higgsfield":
                result = await self.call_higgsfield(task.prompt)
            
            if result:
                task.result = result
                task.status = "completed"
                task.completed_at = datetime.now().isoformat()
                break
            else:
                print(f"  -> {provider} failed, trying next...")
        
        if not task.result:
            task.status = "failed"
        
        # Save to DB
        self.conn.execute("""
            INSERT INTO tasks (task_type, provider_chain, prompt, status, result, created_at, completed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (task.task_type, json.dumps(task.provider_chain), task.prompt, task.status,
              json.dumps(task.result) if task.result else None, task.created_at, task.completed_at))
        self.conn.commit()
        
        return task

async def main():
    """Test the orchestrator with all APIs"""
    orch = AgentOrchestrator()
    
    print("=" * 60)
    print("QUILLYOS AGENT ORCHESTRATOR — API INTEGRATION TEST")
    print("=" * 60)
    
    # Test 1: Content generation (Zhipu -> Gemini -> OpenRouter fallback)
    print("\n[Test 1] Content Generation")
    task = AgentTask(
        id=1,
        task_type="content",
        provider_chain=["zhipu", "gemini", "openrouter"],
        prompt="Write a 30-second TikTok script for a portable charger. Hook in first 3 seconds, casual tone.",
        created_at=datetime.now().isoformat()
    )
    result = await orch.execute_task(task)
    print(f"Result: {result.result[:100]}..." if result.result else "All providers failed")
    
    # Test 2: Research (Tavily -> Brave)
    print("\n[Test 2] Research")
    task = AgentTask(
        id=2,
        task_type="research",
        provider_chain=["tavily", "brave"],
        prompt="best portable chargers 2026",
        created_at=datetime.now().isoformat()
    )
    result = await orch.execute_task(task)
    print(f"Result: {str(result.result)[:100]}..." if result.result else "All providers failed")
    
    # Test 3: Distribution (Telegram)
    print("\n[Test 3] Distribution")
    task = AgentTask(
        id=3,
        task_type="distribution",
        provider_chain=["telegram"],
        prompt="🔥 Just discovered the best portable charger! Link in bio 👆",
        created_at=datetime.now().isoformat()
    )
    result = await orch.execute_task(task)
    print(f"Result: {'Sent' if result.result else 'Failed'}")
    
    print("\n" + "=" * 60)
    print("All tests complete. Check agent_state.db for full logs.")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
