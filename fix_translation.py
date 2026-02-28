import requests
import json
import base64
import time

# Credentials (Hardcoded for Fix)
WP_URL = "https://luckybetvip.com"
WP_USERNAME = "admin"
WP_PASSWORD = "4SvP8Q4hqfxnsDo6xS351Xcr"

# --- Hardcoded English Content (High-Roller Style) ---
NEW_TITLE = "Winning Strategies for Aviator 2026: Complete Guide & Tips"
NEW_SLUG = "winning-strategies-aviator-2026-guide"

HTML_CONTENT = """
<div class="quick-fact-box">
    <div class="fact-item"><strong>Game:</strong> Aviator</div>
    <div class="fact-item"><strong>RTP:</strong> 97%</div>
    <div class="fact-item"><strong>Volatility:</strong> Low-Medium</div>
</div>

<p>The Aviator crash game has dominated the Indian iGaming scene in 2026. Players are no longer relying on pure luck; they are using data-driven strategies to maximize their profits. In this guide, we reveal the top-tier tactics used by high rollers to consistently win at Aviator.</p>

<div class="cta-container" style="text-align:center; margin: 30px 0;">
    <a href="https://1win.com/reg" class="cta-button pulsing-btn">🚀 PLAY AVIATOR NOW & WIN ₹25,000</a>
</div>

<h2> insider Secrets: The 2026 Algorithm Analysis</h2>
<p>Unlike traditional slots, Aviator operates on a "Provably Fair" system. However, experienced players have noticed specific patterns in the RNG (Random Number Generator) that can be exploited for better consistency.</p>

<div class="glass-card">
    <h3>Strategy #1: The Double Bet Method</h3>
    <p>This is the most popular strategy among pros. You place two bets simultaneously:</p>
    <ul>
        <li><strong>Bet 1 (Recovery):</strong> A larger amount (e.g., ₹1000) with a low multiplier target (1.50x). This safer bet covers the cost of both wages.</li>
        <li><strong>Bet 2 (Profit):</strong> A smaller amount (e.g., ₹200) aimed at a high multiplier (5x-10x). If the plane flies high, this is pure profit.</li>
    </ul>
    <p><em>Risk Level: Medium | Potential Return: High</em></p>
</div>

<br>

<div class="glass-card">
    <h3>Strategy #2: The 1.5x Scalping Tactic</h3>
    <p>Slow and steady wins the race. This strategy involves placing a single bet and consistently cashing out at exactly 1.50x.</p>
    <p>Mathematically, the plane exceeds 1.50x roughly 70% of the time, making this a statistically favorable approach for building a bankroll over time.</p>
    <p><em>Risk Level: Low | Potential Return: Consistent</em></p>
</div>

<h2>Pros & Cons of Using Strategies</h2>

<div class="pros-cons-grid">
    <div class="pros-list">
        <h3>Pros</h3>
        <ul>
            <li>Significantly reduces the house edge.</li>
            <li>Allows for better bankroll management.</li>
            <li>Keeps emotional betting in check.</li>
            <li>Double Bet method covers losses effectively.</li>
        </ul>
    </div>
    <div class="cons-list">
        <h3>Cons</h3>
        <ul>
            <li>No strategy guarantees a 100% win rate.</li>
            <li>Requires discipline and patience.</li>
            <li>Fast internet connection is mandatory.</li>
        </ul>
    </div>
</div>

<h2>Key Rules for Success in 2026</h2>
<p>Before you start playing with real money, follow these golden rules:</p>
<ul>
    <li>🎯 <strong>Set a Stop-Loss:</strong> Never chase losses. Decide how much you are willing to lose before you start.</li>
    <li>🎯 <strong>Avoid the "Martingale":</strong> Doubling your bet after a loss can deplete your bankroll quickly in a crash game.</li>
    <li>🎯 <strong>Use Auto-Cashout:</strong> Removes human error and hesitation. Set it and forget it.</li>
</ul>

<h2>FAQ</h2>
<h3>Is Aviator rigged?</h3>
<p>No, Aviator uses Provably Fair cryptographic technology, ensuring that every round's result is transparent and verifiable.</p>

<h3>What is the best time to play Aviator?</h3>
<p>Since the game is RNG-based, there is no "best" time. However, playing during peak hours means more players, which can make the social aspect more engaging.</p>

<h3>Can I hack Aviator?</h3>
<p>No. Any software claiming to "predict" Aviator rounds is a scam. Rely on strategy and bankroll management instead.</p>

<div class="cta-container" style="text-align:center; margin: 30px 0;">
    <a href="https://1win.com/reg" class="cta-button pulsing-btn">💰 CLAIM YOUR 500% WELCOME BONUS</a>
</div>
"""

def find_target_post():
    title_fragment = "Winning Strategies for Aviator 2026"  # Part of the original title
    alt_fragment = "Полный обзор"                      # Part of the Russian title
    
    print(f"🔍 Searching for post containing: '{title_fragment}'...")
    auth = base64.b64encode(f"{WP_USERNAME}:{WP_PASSWORD}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{WP_URL}/wp-json/wp/v2/posts?search={title_fragment}", headers=headers)
    
    if response.status_code == 200:
        posts = response.json()
        if posts:
            for p in posts:
                print(f" - Found Post {p['id']}: {p['title']['rendered']}")
                if alt_fragment in p['title']['rendered'] or "Winning Strategies" in p['title']['rendered']:
                    # Ensure it's not the "Hints & Tricks" post
                    if "Hints & Tricks" not in p['title']['rendered']:
                        return p['id'], p['title']['rendered']
    return None, None

def update_post(post_id, title, content, slug):
    print(f"📝 Updating Post ID {post_id} with new English content...")
    auth = base64.b64encode(f"{WP_USERNAME}:{WP_PASSWORD}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json"
    }
    
    data = {
        "title": title,
        "content": content,
        "slug": slug,
        "status": "publish"
    }
    
    response = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{post_id}", headers=headers, json=data)
    
    if response.status_code == 200:
        print(f"✅ Success! Post Updated.")
        print(f"🔗 Link: {response.json().get('link')}")
    else:
        print(f"❌ Failed to update: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    pid, old_title = find_target_post()
    if pid:
        print(f"🎯 Target Found: ID {pid} ('{old_title}')")
        update_post(pid, NEW_TITLE, HTML_CONTENT, NEW_SLUG)
    else:
        print("❌ Could not find the specific post. Please check the title search terms.")
