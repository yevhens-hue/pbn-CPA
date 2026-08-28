#!/usr/bin/env python3
"""
Creates cornerstone pages + Privacy Policy + Terms & Conditions
in WordPress via REST API.
"""
import requests, base64, os, sys
from dotenv import load_dotenv

load_dotenv()

SITE_URL  = "https://luckybetvip.com"
LOGIN     = "admin"
PASSWORD  = os.getenv("LUCKYBETVIP_APP_PASSWORD", "")

# If not in .env, read from sites_data.json
if not PASSWORD:
    import json
    try:
        with open("data/sites_data.json") as f:
            for s in json.load(f):
                if "luckybetvip" in s.get("url",""):
                    PASSWORD = s.get("app_password","")
                    break
    except Exception:
        pass

if not PASSWORD:
    # Try reading from Google Sheet env or local fallback
    PASSWORD = os.getenv("WP_APP_PASSWORD", "")

AUTH = base64.b64encode(f"{LOGIN}:{PASSWORD}".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {AUTH}",
    "Content-Type": "application/json"
}

# ----------------------------------------------------------------
# PAGE CONTENT DEFINITIONS
# ----------------------------------------------------------------
PAGES = [
    # ---- CORNERSTONE PAGES ----
    {
        "slug":  "aviator-guide",
        "title": "Aviator Game Complete Guide India 2026",
        "content": """
<div class="glass-card">
<h1>✈️ Complete Aviator Game Guide for India Players 2026</h1>
<p>Welcome to the ultimate Aviator game guide for Indian players. This cornerstone resource covers everything you need to know — from basic rules to advanced strategies — to maximize your winnings at Aviator in 2026.</p>
</div>

<div class="glass-card">
<h2>🎯 What is the Aviator Game?</h2>
<p>Aviator is a <strong>crash gambling game</strong> developed by Spribe. A plane takes off and a multiplier grows from 1x upward. Your goal is to cash out <em>before</em> the plane flies away. The game features a 97% RTP and is fully provably fair.</p>
<div class="quick-fact-box">
<div class="fact-item"><strong>RTP:</strong> 97%</div>
<div class="fact-item"><strong>Min Bet:</strong> ₹10</div>
<div class="fact-item"><strong>Max Win:</strong> x100,000</div>
<div class="fact-item"><strong>Provider:</strong> Spribe</div>
</div>
</div>

<div class="glass-card">
<h2>📊 Top Aviator Strategies for India 2026</h2>
<ul>
<li><strong>Low Risk (x1.20–x1.50):</strong> Cash out early every round. Perfect for beginners. Win rate ~80%.</li>
<li><strong>Medium Risk (x2–x5):</strong> Wait for momentum, cash out at 2x–5x. Balanced approach.</li>
<li><strong>High Risk (x10+):</strong> Ride big multipliers. Use auto-cashout to protect gains.</li>
<li><strong>Martingale:</strong> Double stake after each loss. Requires large bankroll.</li>
</ul>
</div>

<div class="glass-card">
<h2>🏆 Best Aviator Sites in India</h2>
<table>
<tr><th>Casino</th><th>Bonus</th><th>Min Deposit</th><th>UPI</th></tr>
<tr><td>1win</td><td>500% up to ₹75,000</td><td>₹300</td><td>✅</td></tr>
<tr><td>Parimatch</td><td>150% up to ₹15,000</td><td>₹200</td><td>✅</td></tr>
<tr><td>Mostbet</td><td>125% up to ₹34,000</td><td>₹300</td><td>✅</td></tr>
</table>
</div>

<div class="cta-container">
[play_aviator]
</div>

<div class="glass-card">
<h2>❓ Frequently Asked Questions</h2>
<h3>Is Aviator legal in India?</h3>
<p>Aviator is available on offshore licensed casinos. Indian laws do not explicitly ban online gambling on foreign sites, so playing Aviator is at your own risk and discretion.</p>
<h3>What is the best strategy for Aviator in India?</h3>
<p>For beginners, the x1.20–x1.50 low-risk auto-cashout strategy offers the highest win rate. Advanced players prefer double-bet strategies split between early and late cashout.</p>
<h3>Can I play Aviator with UPI?</h3>
<p>Yes — 1win, Parimatch, and most listed casinos support UPI deposits and withdrawals for Indian players.</p>
</div>
""",
    },
    {
        "slug":  "cricket-betting-guide",
        "title": "Cricket Betting Guide India 2026 — IPL & T20 Tips",
        "content": """
<div class="glass-card">
<h1>🏏 Complete Cricket Betting Guide for India 2026</h1>
<p>India's most comprehensive cricket betting guide. Everything from understanding odds to advanced IPL betting strategies for the 2026 season.</p>
</div>

<div class="glass-card">
<h2>📌 Cricket Betting Basics</h2>
<ul>
<li><strong>Match Winner:</strong> Bet on which team wins the match.</li>
<li><strong>Top Batsman/Bowler:</strong> Predict the top scorer or wicket-taker.</li>
<li><strong>Over/Under Runs:</strong> Bet if total runs will be above or below a set line.</li>
<li><strong>Live Betting:</strong> Place bets during the match as odds shift.</li>
</ul>
</div>

<div class="glass-card">
<h2>🏆 IPL 2026 Betting Tips</h2>
<p>IPL 2026 runs from March to May. Key factors to consider when betting:</p>
<ul>
<li>Home advantage — teams perform 15% better at home stadiums</li>
<li>Pitch reports — flat pitches favor batsmen, seam-friendly pitches favor bowlers</li>
<li>Toss impact — teams batting second win ~55% of matches in T20</li>
<li>Player form — check last 5-match averages before betting</li>
</ul>
</div>

<div class="cta-container">
[play_aviator]
</div>
""",
    },
    {
        "slug":  "teen-patti-guide",
        "title": "Teen Patti Real Money Guide India 2026",
        "content": """
<div class="glass-card">
<h1>🃏 Ultimate Teen Patti Real Money Guide 2026</h1>
<p>Teen Patti is India's most popular card game. This guide teaches you how to play, win, and choose the best Teen Patti apps for real money in India.</p>
</div>

<div class="glass-card">
<h2>📋 Teen Patti Rules</h2>
<ul>
<li>3 cards are dealt to each player from a standard 52-card deck</li>
<li>Players call (match the bet) or raise (increase) each round</li>
<li>Best hand wins — rankings: Trail > Pure Sequence > Sequence > Color > Pair > High Card</li>
<li>Sideshow option lets you privately compare hands with the previous player</li>
</ul>
</div>

<div class="glass-card">
<h2>💡 Winning Strategies</h2>
<ul>
<li><strong>Blind play:</strong> Play blind for 2–3 rounds to keep pot odds high</li>
<li><strong>Tight-aggressive:</strong> Only enter pots with strong starting hands</li>
<li><strong>Bluffing:</strong> Use sparingly — Indian players call more often</li>
<li><strong>Bankroll management:</strong> Never risk more than 5% per session</li>
</ul>
</div>

<div class="cta-container">
[play_aviator]
</div>
""",
    },
    {
        "slug":  "rummy-guide",
        "title": "Online Rummy Real Money Guide India 2026",
        "content": """
<div class="glass-card">
<h1>🃏 Online Rummy Guide: Win Real Money in India 2026</h1>
<p>Rummy is a skill-based card game where strategy beats luck. This guide covers rules, winning tips, and the best real money Rummy apps for Indian players.</p>
</div>

<div class="glass-card">
<h2>📋 Rummy Rules (Points Rummy)</h2>
<ul>
<li>13 cards dealt to each player from 2 decks (including wild jokers)</li>
<li>Form valid sets (3+ cards of same rank) and sequences (3+ consecutive same-suit cards)</li>
<li>Must have at least 2 sequences including 1 pure sequence (no joker)</li>
<li>First player to declare a valid hand wins</li>
</ul>
</div>

<div class="glass-card">
<h2>💡 Pro Rummy Tips</h2>
<ul>
<li><strong>Priority:</strong> Build your pure sequence first before any other combination</li>
<li><strong>High card risk:</strong> Discard high-value cards (J, Q, K, A) early if unused</li>
<li><strong>Watch discards:</strong> Track what opponents discard to avoid feeding their hand</li>
<li><strong>Joker usage:</strong> Use jokers to complete runs, not pure sequences</li>
</ul>
</div>

<div class="cta-container">
[play_aviator]
</div>
""",
    },

    # ---- LEGAL PAGES ----
    {
        "slug":  "privacy-policy",
        "title": "Privacy Policy — LuckyBetVIP",
        "type":  "page",
        "content": """
<div class="glass-card">
<h1>Privacy Policy</h1>
<p><strong>Last updated:</strong> February 2026</p>

<h2>1. Information We Collect</h2>
<p>LuckyBetVIP.com ("we", "our", "us") collects the following information when you visit our site:</p>
<ul>
<li>Usage data (pages visited, time on site) via cookies and analytics</li>
<li>Device information (browser type, IP address) for security purposes</li>
<li>No personally identifiable information is collected without your explicit consent</li>
</ul>

<h2>2. How We Use Information</h2>
<ul>
<li>To improve website performance and user experience</li>
<li>To serve relevant content and affiliate offers</li>
<li>To comply with legal obligations</li>
</ul>

<h2>3. Cookies</h2>
<p>We use cookies to track your preferences and affiliate referrals. You may disable cookies in your browser settings. Some features of the site may not work properly without cookies.</p>

<h2>4. Third-Party Links</h2>
<p>Our site contains links to third-party gambling sites. We are not responsible for the privacy practices of those sites. We encourage you to review their privacy policies before registering.</p>

<h2>5. Gambling Disclaimer</h2>
<p>All content on LuckyBetVIP is for entertainment and informational purposes only. Online gambling involves risk. Only gamble with money you can afford to lose. If you have a gambling problem, please contact <a href="https://www.gamcare.org.uk" rel="nofollow">GamCare</a>.</p>

<h2>6. Contact Us</h2>
<p>For privacy-related queries, contact us at: <strong>support@luckybetvip.com</strong></p>
</div>
""",
    },
    {
        "slug":  "terms-and-conditions",
        "title": "Terms & Conditions — LuckyBetVIP",
        "type":  "page",
        "content": """
<div class="glass-card">
<h1>Terms & Conditions</h1>
<p><strong>Last updated:</strong> February 2026</p>

<h2>1. Acceptance of Terms</h2>
<p>By accessing LuckyBetVIP.com, you agree to be bound by these Terms & Conditions. If you do not agree, please do not use this website.</p>

<h2>2. Affiliate Disclosure</h2>
<p>LuckyBetVIP.com is an affiliate marketing website. We earn commissions when you click on our links and register at partner gambling sites. All recommendations are honest and based on our editorial assessment.</p>

<h2>3. Age Restriction</h2>
<p>This website is intended for users aged 18 and above only. Do not use this site if you are under the legal gambling age in your jurisdiction.</p>

<h2>4. Responsible Gambling</h2>
<ul>
<li>Set deposit limits at every casino you join</li>
<li>Never chase losses</li>
<li>Take breaks from gambling regularly</li>
<li>Use self-exclusion tools if needed</li>
</ul>

<h2>5. Disclaimer of Warranties</h2>
<p>Content on this site is provided "as is" for informational purposes. While we strive for accuracy, we make no warranties regarding the completeness or accuracy of gambling-related information. Odds and bonuses change frequently — always verify directly with the operator.</p>

<h2>6. Limitation of Liability</h2>
<p>LuckyBetVIP.com shall not be liable for any losses incurred as a result of gambling activities undertaken after visiting this site.</p>

<h2>7. Governing Law</h2>
<p>These terms are governed by and construed in accordance with internationally applicable law. Any disputes shall be resolved through binding arbitration.</p>
</div>
""",
    },
]


def create_page(page_def):
    post_type = page_def.get("type", "post")  # "page" for legal, "post" for guides
    endpoint = f"{SITE_URL}/wp-json/wp/v2/{post_type}s"

    # Check if page already exists by slug
    check = requests.get(
        f"{endpoint}?slug={page_def['slug']}&_fields=id,slug",
        headers=HEADERS, timeout=15
    )
    if check.status_code == 200 and check.json():
        print(f"   ⚠️  Already exists: /{page_def['slug']}/ (skipping)")
        return check.json()[0].get("id")

    payload = {
        "title":   page_def["title"],
        "slug":    page_def["slug"],
        "content": page_def["content"].strip(),
        "status":  "publish",
    }
    resp = requests.post(endpoint, headers=HEADERS, json=payload, timeout=30)
    if resp.status_code in (200, 201):
        data = resp.json()
        print(f"   ✅ Created: {data.get('link', '')}")
        return data.get("id")
    else:
        print(f"   ❌ Failed ({resp.status_code}): {resp.text[:200]}")
        return None


if __name__ == "__main__":
    if not PASSWORD:
        print("❌ No WordPress App Password found. Set LUCKYBETVIP_APP_PASSWORD in .env")
        sys.exit(1)

    print(f"🚀 Creating pages on {SITE_URL}...\n")
    for page in PAGES:
        label = "PAGE" if page.get("type") == "page" else "POST"
        print(f"[{label}] {page['title']}")
        create_page(page)

    print("\n✅ Done! Cornerstone pages and legal pages created.")
    print("   Remember to create /aviator-guide/ as a WP Page (not post) if needed.")
