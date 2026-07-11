"""Content generation module. Uses LLM to create posts from discovered content."""
import httpx, json
from pathlib import Path

HOME = Path("/data/data/com.termux/files/home")
KEYS = HOME / ".quillyos" / "keys"

def load_key(name):
    kf = KEYS / f"{name}.key"
    return kf.read_text().strip() if kf.exists() else None

async def generate_post(content_summary, provider="openrouter"):
    """Generate a Telegram-ready post from content summary."""
    key = load_key(provider)
    if not key:
        return f"[Manual post] {content_summary[:200]}..."

    prompt = f"""Create a short, engaging Telegram post (under 300 chars) about:
{content_summary}

Include a catchy headline and 1-2 sentences. Add relevant hashtags."""

    if provider == "openrouter":
        async with httpx.AsyncClient() as client:
            r = await client.post("https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "HTTP-Referer": "https://quillyos.dev"},
                json={"model": "openai/gpt-3.5-turbo", "messages": [
                    {"role": "user", "content": prompt}
                ]})
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]

    elif provider == "groq":
        async with httpx.AsyncClient() as client:
            r = await client.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}"},
                json={"model": "llama3-8b-8192", "messages": [
                    {"role": "user", "content": prompt}
                ]})
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]

    return f"[Generated via {provider}] {content_summary[:200]}..."

if __name__ == "__main__":
    import asyncio
    post = asyncio.run(generate_post("AI breakthrough in quantum computing announced today."))
    print(post)
