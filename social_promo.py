#!/usr/bin/env python3
"""
social_promo.py — Automated Social Traffic Generator
====================================================
Fetches published articles from WordPress and promotes them on:
1. Telegram channel (auto)
2. Telegra.ph (auto, via API) - Better alternative to Medium
3. Generates Quora answer templates (copy-paste)

Setup:
  .env needs:
    TELEGRAM_BOT_TOKEN=...
    TELEGRAM_CHAT_ID=...
    TELEGRAPH_ACCESS_TOKEN=... # Get one via https://api.telegra.ph/createAccount?short_name=LuckyBet

Usage:
  python3 social_promo.py                 # Promote 1 latest article
  python3 social_promo.py --all           # Promote all unpromoted articles
  python3 social_promo.py --telegram      # Telegram only
  python3 social_promo.py --telegraph     # Telegra.ph only
  python3 social_promo.py --reddit        # Reddit only
  python3 social_promo.py --quora         # Generate Quora templates
"""

import os, sys, json, requests, base64, time, re
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
SITE_URL   = "https://luckybetvip.com"
WP_LOGIN   = "admin"
WP_PASS    = "4SvP8Q4hqfxnsDo6xS351Xcr"

TG_TOKEN   = os.getenv("TELEGRAM_BOT_TOKEN", "")
TG_CHAT    = os.getenv("TELEGRAM_CHAT_ID", "")

# Reddit Config
REDDIT_CLIENT_ID     = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USER         = os.getenv("REDDIT_USERNAME", "")
REDDIT_PASS         = os.getenv("REDDIT_PASSWORD", "")

TELEGRAPH_TOKEN = os.getenv("TELEGRAPH_ACCESS_TOKEN", "")

WP_AUTH = base64.b64encode(f"{WP_LOGIN}:{WP_PASS}".encode()).decode()
WP_HEADERS = {"Authorization": f"Basic {WP_AUTH}"}


# ── Fetch WordPress Posts ─────────────────────────────────────────────────────
def fetch_wp_posts(count=10):
    """Fetches recently published articles from WordPress."""
    resp = requests.get(
        f"{SITE_URL}/wp-json/wp/v2/posts",
        headers=WP_HEADERS,
        params={"per_page": count, "status": "publish", "orderby": "date", "order": "desc",
                "_fields": "id,title,link,excerpt,date,categories"},
        timeout=30
    )
    if resp.status_code != 200:
        print(f"❌ Failed to fetch WP posts: {resp.status_code}")
        return []
    posts = resp.json()
    print(f"✅ Fetched {len(posts)} articles from WordPress")
    return posts


def clean_html(raw):
    """Strip HTML tags from text."""
    text = re.sub(r'<[^>]+>', '', raw)
    return re.sub(r'\s+', ' ', text).strip()


# ── TELEGRAM ──────────────────────────────────────────────────────────────────
def post_to_telegram(post, delay=0):
    """Sends an article announcement to Telegram channel."""
    if not TG_TOKEN or not TG_CHAT:
        print("⚠️  Telegram not configured. Add TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID to .env")
        return False

    title   = clean_html(post['title']['rendered'])
    link    = post['link']
    excerpt = clean_html(post.get('excerpt', {}).get('rendered', ''))[:200]
    topic   = title.lower()

    # Pick emoji by topic
    if 'cricket' in topic or 'ipl' in topic:
        emoji = '🏏'
    elif 'teen patti' in topic or 'patti' in topic:
        emoji = '🃏'
    elif 'rummy' in topic:
        emoji = '🀄'
    elif 'aviator' in topic:
        emoji = '✈️'
    else:
        emoji = '🎰'

    msg = (
        f"{emoji} *{title}*\n\n"
        f"_{excerpt}..._\n\n"
        f"🔗 [Read Full Article]({link})\n\n"
        f"💡 Expert tips for Indian players. Tap the link above! 👆\n"
        f"#India #Gaming #Casino #Aviator"
    )

    if delay:
        time.sleep(delay)

    resp = requests.post(
        f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
        json={"chat_id": TG_CHAT, "text": msg, "parse_mode": "Markdown",
              "disable_web_page_preview": False},
        timeout=10
    )
    if resp.status_code == 200:
        print(f"  ✈️  Telegram: Posted '{title[:50]}'")
        return True
    else:
        print(f"  ❌ Telegram error: {resp.status_code} {resp.text[:100]}")
        return False


# ── TELEGRA.PH ────────────────────────────────────────────────────────────────
def post_to_telegraph(post):
    """Cross-posts article to Telegra.ph via their API."""
    if not TELEGRAPH_TOKEN:
        print("⚠️  Telegra.ph not configured. Add TELEGRAPH_ACCESS_TOKEN to .env")
        print("    Create one by visiting: https://api.telegra.ph/createAccount?short_name=LuckyBet&author_name=LuckyBetVIP")
        return False

    title   = clean_html(post['title']['rendered'])
    link    = post['link']
    excerpt = clean_html(post.get('excerpt', {}).get('rendered', ''))

    # Telegra.ph content must be a JSON array of Node objects
    content_nodes = [
        {"tag": "h3", "children": [title]},
        {"tag": "p", "children": [excerpt]},
        {"tag": "p", "children": [
            {"tag": "strong", "children": [
                {"tag": "a", "attrs": {"href": link}, "children": ["Read the full article on LuckyBetVIP.com →"]}
            ]}
        ]},
        {"tag": "hr"},
        {"tag": "p", "children": [
            {"tag": "em", "children": ["Originally published at "]},
            {"tag": "a", "attrs": {"href": link}, "children": [link]}
        ]}
    ]

    payload = {
        "access_token": TELEGRAPH_TOKEN,
        "title":        title,
        "author_name":  "LuckyBetVIP",
        "author_url":   SITE_URL,
        "content":      json.dumps(content_nodes),
        "return_content": False
    }

    resp = requests.post(
        "https://api.telegra.ph/createPage",
        data=payload,
        timeout=30
    )
    
    if resp.status_code == 200:
        data = resp.json()
        if data.get("ok"):
            telegraph_url = data.get("result", {}).get("url", "")
            print(f"  🚀 Telegra.ph: Published → {telegraph_url}")
            return True
        else:
            print(f"  ❌ Telegra.ph error: {data.get('error')}")
            return False
    else:
        print(f"  ❌ Telegra.ph request failed: {resp.status_code}")
        return False


# ── REDDIT ────────────────────────────────────────────────────────────────────
def get_reddit_token():
    """Obtains an OAuth2 token from Reddit."""
    if not all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER, REDDIT_PASS]):
        return None
    
    auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)
    data = {
        'grant_type': 'password',
        'username': REDDIT_USER,
        'password': REDDIT_PASS
    }
    headers = {'User-Agent': 'LuckyBetVIPBot/0.1 by ' + REDDIT_USER}
    
    try:
        resp = requests.post("https://www.reddit.com/api/v1/access_token", 
                             auth=auth, data=data, headers=headers, timeout=15)
        if resp.status_code == 200:
            return resp.json().get('access_token')
        else:
            print(f"  ❌ Reddit Token Error: {resp.status_code} {resp.text[:100]}")
    except Exception as e:
        print(f"  ❌ Reddit Auth Exception: {e}")
    return None

def post_to_reddit(post, subreddit="CasinoIndia"):
    """Posts article link to a specific subreddit."""
    token = get_reddit_token()
    if not token:
        print("⚠️  Reddit not configured. Add REDDIT_CLIENT_ID, SECRET, USER, PASS to .env")
        return False

    title = clean_html(post['title']['rendered'])
    link  = post['link']
    
    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': f'LuckyBetVIPBot/0.1 by {REDDIT_USER}'
    }
    
    payload = {
        'sr':    subreddit,
        'kind':  'link',
        'title': title,
        'url':   link,
        'resubmit': True
    }
    
    try:
        resp = requests.post("https://oauth.reddit.com/api/submit", 
                             headers=headers, data=payload, timeout=20)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('json', {}).get('errors'):
                print(f"  ❌ Reddit Error in {subreddit}: {data['json']['errors']}")
                return False
            print(f"  🔥 Reddit: Posted to r/{subreddit} → {title[:40]}")
            return True
        else:
            print(f"  ❌ Reddit HTTP Error: {resp.status_code} {resp.text[:100]}")
    except Exception as e:
        print(f"  ❌ Reddit Exception: {e}")
    return False


# ── QUORA TEMPLATES ───────────────────────────────────────────────────────────
QUORA_QUESTIONS = {
    "aviator": [
        "What is the best strategy for the Aviator game in India?",
        "How do I win at Aviator crash game?",
        "Is Aviator game real or fake in India?",
        "What is the best time to play Aviator game?",
        "How to withdraw money from Aviator game in India?",
    ],
    "cricket": [
        "What are the best cricket betting tips for IPL 2026?",
        "Which is the best cricket betting app in India?",
        "How do I bet on cricket online in India?",
    ],
    "teen patti": [
        "What are the best Teen Patti strategies to win?",
        "Which is the best Teen Patti app for real money in India?",
    ],
    "rummy": [
        "How to win at Rummy online in India?",
        "What is the pure sequence rule in Rummy?",
    ]
}

def generate_quora_templates(posts):
    """Generates Quora answer templates for manual posting."""
    print("\n" + "="*60)
    print("📋 QUORA ANSWER TEMPLATES (copy-paste manually)")
    print("="*60)

    for post in posts[:5]:
        title   = clean_html(post['title']['rendered'])
        link    = post['link']
        excerpt = clean_html(post.get('excerpt', {}).get('rendered', ''))[:300]
        topic   = title.lower()

        # Match question
        question = None
        for key, questions in QUORA_QUESTIONS.items():
            if key in topic:
                question = questions[0]
                break
        if not question:
            question = f"What is the best strategy for online gaming in India 2026?"

        print(f"\n📌 Article: {title}")
        print(f"   Quora question to answer: \"{question}\"")
        print(f"   Suggested answer:")
        print(f"   ---")
        print(f"   Great question! I've been playing for a while and here's what works:")
        print(f"   {excerpt}")
        print(f"   I wrote a detailed guide covering this: {link}")
        print(f"   Hope this helps! 🙏")
        print(f"   ---")

    print("\n" + "="*60)
    print("Also post on Reddit threads:")
    print("  r/IndianGaming, r/Cricket, r/india, r/CasinoIndia")
    print("="*60)


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    args = sys.argv[1:]
    do_all       = "--all"       in args
    do_telegram  = "--telegram"  in args or not args
    do_telegraph = "--telegraph" in args or not args
    do_reddit    = "--reddit"    in args or not args
    do_quora     = "--quora"     in args or not args

    count = 5 if do_all else 1
    posts = fetch_wp_posts(count=count)
    if not posts:
        print("No articles found.")
        return

    print(f"\n📣 Promoting {len(posts)} article(s)...\n")

    for i, post in enumerate(posts):
        title = clean_html(post['title']['rendered'])
        print(f"\n[{i+1}/{len(posts)}] {title[:70]}")

        if do_telegram:
            post_to_telegram(post, delay=2 if i > 0 else 0)

        if do_telegraph:
            post_to_telegraph(post)
            time.sleep(1)  # Brief pause between posts

        if do_reddit:
            # We target specific subreddits for Indian gambling/gaming
            subreddits = ["CasinoIndia", "IndianGaming"]
            for sub in subreddits:
                post_to_reddit(post, subreddit=sub)
                time.sleep(5)  # Avoid spam filters

    if do_quora:
        generate_quora_templates(posts)

    print(f"\n✅ Promotion done! Processed {len(posts)} articles.")


if __name__ == "__main__":
    main()
