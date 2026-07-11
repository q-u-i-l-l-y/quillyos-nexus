"""Unified UGC pipeline: Discover → Generate → Distribute."""
import asyncio, sys
from discover import discover_all
from generate import generate_post
from distribute import post_to_telegram

async def run_pipeline(topic="technology trends"):
    print("[1/3] Discovering content...")
    discovered = await discover_all()

    # Pick best content (simple: first Tavily result)
    sources = discovered.get("tavily", [])
    if not sources:
        print("[!] No content discovered")
        return

    best = sources[0]
    summary = f"{best.get('title', 'No title')}: {best.get('content', best.get('url', ''))}"
    print(f"  → {summary[:100]}...")

    print("[2/3] Generating post...")
    post = await generate_post(summary)
    print(f"  → {post[:100]}...")

    print("[3/3] Distributing...")
    # Uncomment when ready to post live:
    # await post_to_telegram(post)
    print("  → [DRY RUN] Post ready but not sent. Uncomment to enable live posting.")


    from html_report import generate_report
    generate_report(discovered, post, status="dry-run")
    return post

if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "technology trends"
    result = asyncio.run(run_pipeline(topic))
    if result:
        print("\n[+] Pipeline complete!")
