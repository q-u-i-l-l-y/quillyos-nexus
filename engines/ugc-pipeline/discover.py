"""Content discovery module. Fetches trending topics from multiple sources."""
import httpx, json
from pathlib import Path

HOME = Path("/data/data/com.termux/files/home")
KEYS = HOME / ".quillyos" / "keys"

def load_key(name):
    kf = KEYS / f"{name}.key"
    return kf.read_text().strip() if kf.exists() else None

async def tavily_search(query="technology trends", max_results=3):
    key = load_key("tavily")
    if not key: return []
    async with httpx.AsyncClient() as client:
        r = await client.post("https://api.tavily.com/search",
            json={"api_key": key, "query": query, "max_results": max_results})
        return r.json().get("results", []) if r.status_code == 200 else []

async def hn_top_stories(count=3):
    async with httpx.AsyncClient() as client:
        r = await client.get("https://hacker-news.firebaseio.com/v0/topstories.json")
        if r.status_code != 200: return []
        ids = r.json()[:count]
        stories = []
        for sid in ids:
            sr = await client.get(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json")
            if sr.status_code == 200:
                stories.append(sr.json())
        return stories

async def wikipedia_trending():
    async with httpx.AsyncClient() as client:
        r = await client.get("https://en.wikipedia.org/api/rest_v1/feed/featured")
        return r.json() if r.status_code == 200 else {}

async def discover_all():
    """Run all discovery sources and return combined results."""
    results = {
        "tavily": await tavily_search(),
        "hn": await hn_top_stories(),
        "wikipedia": await wikipedia_trending(),
    }
    return results

if __name__ == "__main__":
    import asyncio
    data = asyncio.run(discover_all())
    print(json.dumps(data, indent=2)[:2000])
