#!/usr/bin/env python3
import os
import json
import sqlite3
import datetime
import random
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "bonuses.db"
OUTPUT_DIR = BASE_DIR.parent / "frontend" / "data" / "blog"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_db_data(geo=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    query = "SELECT * FROM bonuses WHERE is_active = 1"
    params = []
    if geo:
        query += " AND geo = ?"
        params.append(geo)
    rows = c.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def generate_article(topic, geo_context, bonus_data):
    if not GROQ_API_KEY:
        print("GROQ_API_KEY not found. Skipping article generation.")
        return None

    # Format bonus data for the prompt
    bonus_summary = "\n".join([
        f"- {b['brand_name']}: {b['bonus_title']} ({b['bonus_amount']}). Wagering: {b['wagering'] or 'N/A'}. Rating: {b['rating']}/5"
        for b in bonus_data[:5]
    ])

    prompt = f"""
    Write a high-quality SEO-optimized blog article in English for an iGaming affiliate site called 'games-income.com'.
    Topic: {topic}
    Market Context: {geo_context}
    Latest Bonuses to include in a table:
    {bonus_summary}

    Structure requirements (Similar to luckybetvip.com):
    1. Catchy H1 Title (include '2026').
    2. Introduction: engaging and keyword-rich.
    3. H2 Heading: Industry Insights (mention Pragmatic Play or Aviator as popular choices based on @igaming_inside findings).
    4. H2 Heading: Comparative Bonus Table. (Represented as Markdown table).
    5. H2 Heading: Expert Guide on how to claim and use these bonuses.
    6. H3 Heading: Legality and Safety (mention specific {geo_context} context).
    7. Conclusion: Strong CTA.

    Tone: Professional, expert, data-driven.
    Output should be valid JSON with 'title', 'slug', 'content' (Markdown), and 'date' fields.
    """

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        res_json = response.json()
        return json.loads(res_json['choices'][0]['message']['content'])
    except Exception as e:
        print(f"Error generating article: {e}")
        return None

def main():
    topics = [
        {"title": "Best Casino Bonuses in India 2026: Ultimate Guide", "geo": "IN"},
        {"title": "Top Betting Offers in Turkey: Legit Sites and Promos 2026", "geo": "TR"},
        {"title": "Brazil iGaming Boom 2026: Leading Crypto and Casino Bonuses", "geo": "BR"},
        {"title": "No Wager Bonuses: The Future of iGaming in 2026", "geo": "all"},
        {"title": "How to Maximize Your Wins with Aviator Strategies 2026", "geo": "IN"},
        {"name": "Pragmatic Play Slots: Where to Find the Best Free Spins in 2026", "geo": "all"}
    ]
    
    # Pick 2 random topics for today (or rotate)
    selected = random.sample(topics, 2)
    
    for item in selected:
        geo = item.get('geo', 'all')
        if geo == 'all':
            geo_name = "Global"
            bonus_data = get_db_data()
        else:
            geo_name = geo
            bonus_data = get_db_data(geo)
            
        print(f"Generating article: {item['title']}...")
        result = generate_article(item['title'], geo_name, bonus_data)
        
        if result:
            date_str = datetime.datetime.now().strftime("%Y-%m-%d")
            slug = result.get('slug', item['title'].lower().replace(" ", "-").replace(":", ""))
            filename = f"{date_str}-{slug}.json"
            
            with open(OUTPUT_DIR / filename, "w") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"✅ Article saved: {filename}")

if __name__ == "__main__":
    main()
