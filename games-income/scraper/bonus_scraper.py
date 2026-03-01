#!/usr/bin/env python3
"""
games-income.com — Bonus Scraper
Scrapes bonus information from top casino/betting sites by GEO location.

Usage:
    python bonus_scraper.py --geo IN --type casino
    python bonus_scraper.py --geo UA --type betting
    python bonus_scraper.py --geo IN --type all --dry-run
"""

import os
import json
import time
import argparse
import sqlite3
import datetime
import requests
from typing import Optional, List
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
CONFIG_DIR = BASE_DIR / "config"
DB_PATH = BASE_DIR / "bonuses.db"

# ─── Load configs ─────────────────────────────────────────────────────────────
with open(CONFIG_DIR / "sites_by_geo.json", "r") as f:
    SITES_BY_GEO = json.load(f)

with open(CONFIG_DIR / "bonus_selectors.json", "r") as f:
    BONUS_SELECTORS = json.load(f)

# ─── Database ─────────────────────────────────────────────────────────────────

def init_db():
    """Initialize the SQLite database and create the bonuses table."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS bonuses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            geo         TEXT NOT NULL,
            type        TEXT NOT NULL,       -- 'casino' or 'betting'
            brand_id    TEXT NOT NULL,
            brand_name  TEXT NOT NULL,
            bonus_title TEXT,
            bonus_amount TEXT,
            bonus_type  TEXT,               -- 'welcome', 'reload', 'cashback', 'free_spins'
            wagering    TEXT,
            conditions  TEXT,
            affiliate_url TEXT,
            logo_url    TEXT,
            rating      REAL,
            is_active   INTEGER DEFAULT 1,
            scraped_at  TEXT,
            expires_at  TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Database initialized.")


def save_bonuses(bonuses: list):
    """Save scraped bonuses to the database, replacing old ones for same brand+geo."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for b in bonuses:
        # Deactivate old records for this brand+geo+type
        c.execute("""
            UPDATE bonuses SET is_active = 0
            WHERE geo = ? AND brand_id = ? AND type = ?
        """, (b["geo"], b["brand_id"], b["type"]))
        # Insert new
        c.execute("""
            INSERT INTO bonuses
            (geo, type, brand_id, brand_name, bonus_title, bonus_amount, bonus_type,
             wagering, conditions, affiliate_url, logo_url, rating, is_active, scraped_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
        """, (
            b["geo"], b["type"], b["brand_id"], b["brand_name"],
            b.get("bonus_title"), b.get("bonus_amount"), b.get("bonus_type", "welcome"),
            b.get("wagering"), b.get("conditions"),
            b.get("affiliate_url"), b.get("logo_url"), b.get("rating"),
            datetime.datetime.utcnow().isoformat()
        ))
    conn.commit()
    conn.close()
    print(f"💾 Saved {len(bonuses)} bonuses to database.")


def get_bonuses(geo: str = None, bonus_type: str = None) -> list:
    """Query the database for active bonuses."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    query = "SELECT * FROM bonuses WHERE is_active = 1"
    params = []
    if geo:
        query += " AND geo = ?"
        params.append(geo.upper())
    if bonus_type:
        query += " AND type = ?"
        params.append(bonus_type)
    query += " ORDER BY rating DESC"
    rows = c.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── Scraping Logic ───────────────────────────────────────────────────────────

def fetch_page_html(url: str, timeout: int = 20) -> Optional[str]:
    """Fetch raw HTML from a URL using requests."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/121.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        if resp.status_code == 200:
            return resp.text
        print(f"  ⚠️  HTTP {resp.status_code} for {url}")
    except Exception as e:
        print(f"  ❌  Could not fetch {url}: {e}")
    return None


def extract_bonuses_with_ai(html: str, brand_name: str, geo: str) -> list:
    """
    Send HTML to Groq/Gemini AI and ask it to extract bonus data as JSON.
    This is the core intelligence of the scraper.
    """
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        print("  ⚠️  GROQ_API_KEY not set. Cannot use AI extraction.")
        return []
    
    # Strip whitespace to prevent "Invalid header value" errors from malformed secrets
    groq_key = groq_key.strip()

    # Trim HTML to avoid token limits — take first 8000 chars
    html_snippet = html[:8000]

    prompt = f"""You are a data extraction assistant. I will give you an HTML snippet from the promotions/bonuses page of "{brand_name}" casino/betting platform (region: {geo}).

Extract ALL bonus offers you can find. Return ONLY a valid JSON array. Each item must have these fields:
- "bonus_title": string (name of the bonus)
- "bonus_amount": string (e.g., "100% up to ₹10,000", "50 Free Spins", "₹500 Cashback")
- "bonus_type": one of ["welcome", "reload", "cashback", "free_spins", "vip", "sports", "other"]
- "wagering": string (wagering requirements, e.g. "30x" or "N/A")
- "conditions": string (brief conditions summary, max 100 chars)
- "expires_at": string (expiry date if mentioned, else null)

HTML Snippet:
{html_snippet}

Return ONLY the JSON array, no explanation, no markdown code blocks."""

    try:
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {groq_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 2000,
                "temperature": 0.2
            },
            timeout=30
        )
        if resp.status_code == 200:
            raw = resp.json()["choices"][0]["message"]["content"].strip()
            # Extract JSON array from response
            start = raw.find("[")
            end = raw.rfind("]") + 1
            if start >= 0 and end > start:
                return json.loads(raw[start:end])
    except Exception as e:
        print(f"  ⚠️  AI extraction failed: {e}")
    return []


def scrape_site(site: dict, geo: str, bonus_type: str) -> list:
    """Scrape a single site and return list of bonus dicts."""
    print(f"\n  🔍 Scraping {site['name']} ({geo})...")
    html = fetch_page_html(site["bonus_url"])

    if not html:
        print(f"  ⚠️  Falling back to static defaults for {site['name']}")
        return get_fallback_bonuses(site, geo, bonus_type)

    # AI extraction
    ai_bonuses = extract_bonuses_with_ai(html, site["name"], geo)

    if not ai_bonuses:
        print(f"  ⚠️  AI found no bonuses, using fallback for {site['name']}")
        return get_fallback_bonuses(site, geo, bonus_type)

    result = []
    for b in ai_bonuses:
        result.append({
            "geo": geo,
            "type": bonus_type,
            "brand_id": site["brand_id"],
            "brand_name": site["name"],
            "bonus_title": b.get("bonus_title"),
            "bonus_amount": b.get("bonus_amount"),
            "bonus_type": b.get("bonus_type", "welcome"),
            "wagering": b.get("wagering"),
            "conditions": b.get("conditions"),
            "expires_at": b.get("expires_at"),
            "affiliate_url": site.get("affiliate_url"),
            "logo_url": site.get("logo"),
            "rating": site.get("rating", 4.0),
        })
    print(f"  ✅ Found {len(result)} bonuses for {site['name']}")
    return result


def get_fallback_bonuses(site: dict, geo: str, bonus_type: str) -> list:
    """Returns hardcoded fallback bonuses when scraping fails."""
    # Use site-specific or geo-specific defaults
    curr = "₹" if geo == "IN" else "₺" if geo == "TR" else "R$" if geo == "BR" else "$"
    
    FALLBACKS = {
        "1win": {
            "bonus_title": "Welcome Package",
            "bonus_amount": f"500% up to {curr}75,000" if geo == "IN" else f"500% up to {curr}25,000",
            "bonus_type": "welcome"
        },
        "1xbet": {
            "bonus_title": "First Deposit Bonus",
            "bonus_amount": f"100% up to {curr}10,000" if geo == "IN" else f"100% up to {curr}3,500",
            "bonus_type": "welcome"
        },
        "default": {
            "bonus_title": "Welcome Bonus",
            "bonus_amount": f"100% up to {curr}10,000",
            "bonus_type": "welcome",
            "wagering": "30x",
            "conditions": "Refer to website for full terms."
        }
    }
    
    brand_data = FALLBACKS.get(site["brand_id"], FALLBACKS["default"])
    return [{
        "geo": geo,
        "type": bonus_type,
        "brand_id": site["brand_id"],
        "brand_name": site["name"],
        **data,
        "expires_at": None,
        "affiliate_url": site.get("affiliate_url"),
        "logo_url": site.get("logo"),
        "rating": site.get("rating", 4.0),
    }]


# ─── Main Runner ──────────────────────────────────────────────────────────────

def run_scraper(geo: str, bonus_type: str = "all", dry_run: bool = False):
    """Main entry point: scrapes all sites for a given geo and type."""
    geo = geo.upper()
    if geo not in SITES_BY_GEO:
        print(f"❌ GEO '{geo}' not found in config. Available: {list(SITES_BY_GEO.keys())}")
        return

    geo_config = SITES_BY_GEO[geo]
    print(f"\n🌍 Scraping bonuses for {geo_config['name']} ({geo}) — Type: {bonus_type}")
    print("=" * 60)

    all_bonuses = []
    types_to_scrape = ["casino", "betting"] if bonus_type == "all" else [bonus_type]

    for t in types_to_scrape:
        sites = geo_config.get(t, [])
        if not sites:
            print(f"  ℹ️  No {t} sites configured for {geo}")
            continue
        print(f"\n📂 {t.upper()} Sites ({len(sites)} configured):")
        for site in sites:
            bonuses = scrape_site(site, geo, t)
            all_bonuses.extend(bonuses)
            time.sleep(1)  # Polite delay between requests

    print(f"\n{'='*60}")
    print(f"✅ Total bonuses collected: {len(all_bonuses)}")

    if dry_run:
        print("\n🔍 DRY RUN — Not saving to database. Preview:")
        print(json.dumps(all_bonuses, indent=2, ensure_ascii=False))
    else:
        save_bonuses(all_bonuses)
        print("💾 Saved to database.")

    return all_bonuses


# ─── JSON API Export ──────────────────────────────────────────────────────────

def export_json_api(geo: str = None, bonus_type: str = None, output_file: str = None):
    """Export bonuses from DB as JSON (for use as a static API or WordPress feed)."""
    bonuses = get_bonuses(geo, bonus_type)
    output = {
        "updated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "geo": geo or "all",
        "type": bonus_type or "all",
        "count": len(bonuses),
        "bonuses": bonuses
    }
    json_str = json.dumps(output, indent=2, ensure_ascii=False)
    if output_file:
        with open(output_file, "w") as f:
            f.write(json_str)
        print(f"📄 JSON API exported to: {output_file}")
    else:
        print(json_str)
    return output


# ─── CLI Entry ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="games-income.com Bonus Scraper")
    parser.add_argument("--geo",     default="IN",  help="Country code: IN, UA, BR etc.")
    parser.add_argument("--type",    default="all", help="'casino', 'betting' or 'all'")
    parser.add_argument("--dry-run", action="store_true", help="Print results, don't save to DB")
    parser.add_argument("--export",  action="store_true", help="Export current DB to JSON")
    parser.add_argument("--output",  default=None,  help="Output file for --export")
    args = parser.parse_args()

    init_db()

    if args.export:
        export_json_api(geo=args.geo, bonus_type=args.type, output_file=args.output)
    else:
        run_scraper(geo=args.geo, bonus_type=args.type, dry_run=args.dry_run)
