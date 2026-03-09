#!/usr/bin/env python3
"""
games-income.com — Bonus Scraper
Scrapes bonus information from top casino/betting sites by GEO location.

Usage:
    python bonus_scraper.py --geo IN --type casino
    python bonus_scraper.py --geo TR --type betting
    python bonus_scraper.py --geo IN --type all --dry-run
"""

import os
import json
import time
import argparse
import sqlite3
import datetime
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
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
            expires_at  TEXT,
            featured_providers TEXT
        )
    """)
    # Add column if it doesn't exist (for existing databases)
    try:
        c.execute("ALTER TABLE bonuses ADD COLUMN featured_providers TEXT")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()
    print("✅ Database initialized.")


def save_bonuses(bonuses: list):
    """Save scraped bonuses to the database, replacing old ones for same brand+geo."""
    if not bonuses:
        return
        
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get unique (geo, brand_id, type) combinations in the new batch
    affected_sites = set((b["geo"], b["brand_id"], b["type"]) for b in bonuses)
    
    # Deactivate all active bonuses for these sites ONCE
    for geo, brand_id, b_type in affected_sites:
        c.execute("""
            UPDATE bonuses SET is_active = 0
            WHERE geo = ? AND brand_id = ? AND type = ?
        """, (geo, brand_id, b_type))
        
    for b in bonuses:
        # Insert new
        c.execute("""
            INSERT INTO bonuses
            (geo, type, brand_id, brand_name, bonus_title, bonus_amount, bonus_type,
             wagering, conditions, affiliate_url, logo_url, rating, is_active, scraped_at, featured_providers)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
        """, (
            b["geo"], b["type"], b["brand_id"], b["brand_name"],
            b.get("bonus_title"), b.get("bonus_amount"), b.get("bonus_type", "welcome"),
            b.get("wagering"), b.get("conditions"),
            b.get("affiliate_url"), b.get("logo_url"), b.get("rating"),
            datetime.datetime.utcnow().isoformat(),
            b.get("featured_providers")
        ))
    conn.commit()
    conn.close()
    print(f"💾 Saved {len(bonuses)} bonuses to database.")


def get_bonuses(geo: str = None, bonus_type: str = None, include_inactive: bool = False) -> list:
    """Query the database for active (and optionally recent inactive) bonuses."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    query = "SELECT * FROM bonuses WHERE 1=1"
    if not include_inactive:
        query += " AND is_active = 1"
    
    params = []
    if geo:
        query += " AND geo = ?"
        params.append(geo.upper())
    if bonus_type and bonus_type != "all":
        query += " AND type = ?"
        params.append(bonus_type)
        
    query += " ORDER BY is_active DESC, rating DESC"
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
- "featured_providers": string (comma-separated list of game providers mentioned, e.g. "Pragmatic Play, Evolution", or null)

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
        **brand_data,
        "expires_at": None,
        "affiliate_url": site.get("affiliate_url"),
        "logo_url": site.get("logo"),
        "rating": site.get("rating", 4.0),
    }]


# ─── Google Sheets Export ─────────────────────────────────────────────────────

def export_to_sheets(geo: str = None, bonus_type: str = None, clear_sheets: bool = False):
    """
    Export active bonuses from the local DB to the Google Sheet.
    Unified storage: https://docs.google.com/spreadsheets/d/1yQJKYRpdc8I-xRlLYrEgz8hhN1bQYM4NuG7NOUbyqAc/
    """
    json_creds = os.getenv("GOOGLE_CREDENTIALS")
    if not json_creds:
        print("  ⚠️  GOOGLE_CREDENTIALS not set. Skipping Sheets export.")
        return

    sheet_id = "1yQJKYRpdc8I-xRlLYrEgz8hhN1bQYM4NuG7NOUbyqAc"
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    try:
        # Auth with gspread
        if os.path.exists(json_creds):
            creds = ServiceAccountCredentials.from_json_keyfile_name(json_creds, scope)
        else:
            creds_auth = json.loads(json_creds)
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_auth, scope)
        
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(sheet_id)
        
        # We'll use a tab named after the GEO or just 'All'
        tab_name = geo.upper() if geo else "All Bonuses"
        try:
            worksheet = spreadsheet.worksheet(tab_name)
            if clear_sheets:
                # Clear everything to start fresh
                worksheet.clear()
        except gspread.exceptions.WorksheetNotFound:
            # Create if it doesn't exist
            worksheet = spreadsheet.add_worksheet(title=tab_name, rows=1000, cols=15)
        
        # Desired header structure
        headers = [
            "Scraped At", "Status", "ID", "GEO", "Type", "Brand", "Bonus Title", 
            "Amount", "Wagering", "Providers", "Conditions", "Affiliate URL", "Rating"
        ]

        # Get existing data to avoid duplicates (if not cleared)
        existing_rows = worksheet.get_all_values()
        existing_keys = set()

        if clear_sheets or not existing_rows:
            worksheet.append_row(headers)
            # Freeze header
            worksheet.freeze(rows=1)
        else:
            # Check/Fix headers
            if existing_rows[0] != headers:
                worksheet.update("A1", [headers])
            
            # Key indices: Brand(5), Title(6), Amount(7)
            for row in existing_rows[1:]:
                if len(row) >= 8:
                    key = f"{row[5]}|{row[6]}|{row[7]}".strip().lower()
                    existing_keys.add(key)
        
        # Get data from DB
        bonuses = get_bonuses(geo, bonus_type, include_inactive=True)
        
        # Prepare new rows
        new_rows = []
        for b in bonuses:
            brand = b.get("brand_name", "")
            title = b.get("bonus_title", "")
            amount = b.get("bonus_amount", "")
            key = f"{brand}|{title}|{amount}".strip().lower()
            
            if key not in existing_keys:
                status = "ACTIVE" if b.get("is_active") == 1 else "EXPIRED"
                row = [
                    datetime.datetime.fromisoformat(b.get("scraped_at")).strftime("%d.%m.%Y %H:%M") if b.get("scraped_at") else "",
                    status,
                    str(b.get("id") or ""),
                    b.get("geo", ""),
                    b.get("type", ""),
                    brand,
                    title,
                    amount,
                    b.get("wagering", ""),
                    b.get("featured_providers", ""),
                    str(b.get("conditions") or "")[:100],
                    b.get("affiliate_url", ""),
                    b.get("rating", 4.0)
                ]
                new_rows.append(row)
                existing_keys.add(key)

        # If clear_sheets, we overwrite EVERYTHING starting from A1
        if clear_sheets:
            full_data = [headers] + new_rows
            worksheet.update("A1", full_data)
            print(f"🧹 Tab {tab_name} hard-reset with {len(new_rows)} rows.")
        elif new_rows:
            worksheet.append_rows(new_rows)
            print(f"✅ Appended {len(new_rows)} NEW bonuses to Google Sheet (Tab: {tab_name}).")
        else:
            print(f"ℹ️  No new bonuses to append for {tab_name}.")
        
    except Exception as e:
        print(f"  ❌ Google Sheets export failed: {e}")


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
        # Export to Google Sheets for this GEO
        export_to_sheets(geo, bonus_type)

    return all_bonuses


# ─── JSON API Export ──────────────────────────────────────────────────────────

def export_json_api(geo: str = None, bonus_type: str = None, output_file: str = None):
    """Export bonuses from DB as JSON (including New/Expired status logic)."""
    # Fetch both active and recently inactive
    all_bonuses = get_bonuses(geo, bonus_type, include_inactive=True)
    
    now = datetime.datetime.utcnow()
    processed = []
    
    for b in all_bonuses:
        scraped_at = datetime.datetime.fromisoformat(b["scraped_at"])
        age_hours = (now - scraped_at).total_seconds() / 3600
        
        # We only want to export inactive bonuses if they are "Freshly Expired" (within 48h)
        if b["is_active"] == 0 and age_hours > 48:
            continue
            
        b["is_new"] = age_hours < 24 and b["is_active"] == 1
        b["is_expired"] = b["is_active"] == 0
        processed.append(b)

    output = {
        "updated_at": now.isoformat() + "Z",
        "geo": geo or "all",
        "type": bonus_type or "all",
        "count": len(processed),
        "bonuses": processed
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
    parser.add_argument("--export",  action="store_true", help="Export JSON for frontend")
    parser.add_argument("--sheets",  action="store_true", help="Export to Google Sheets")
    parser.add_argument("--clear-sheets", action="store_true", help="Clear sheets before export")
    parser.add_argument("--output",  help="Output file for JSON export")
    args = parser.parse_args()

    init_db()

    if args.sheets:
        export_to_sheets(args.geo, args.type, clear_sheets=args.clear_sheets)
    elif args.export:
        export_json_api(geo=args.geo, bonus_type=args.type, output_file=args.output)
    else:
        run_scraper(geo=args.geo, bonus_type=args.type, dry_run=args.dry_run)
