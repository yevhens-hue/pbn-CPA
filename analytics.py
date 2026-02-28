import json
import os
import csv
import requests
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
DB_FILE = 'data/pbn_metrics.db'
if not os.path.exists('data'):
    os.makedirs('data')

def init_db():
    """
    Initializes the SQLite database with the requested schema.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        # Table for general stats
        c.execute('''CREATE TABLE IF NOT EXISTS publications
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      timestamp DATETIME,
                      success_count INTEGER,
                      error_count INTEGER,
                      links_inserted INTEGER,
                      cost_usd REAL,
                      revenue_usd REAL,
                      quality_score INTEGER DEFAULT 0)''')
        # Table for persona stats
        c.execute('''CREATE TABLE IF NOT EXISTS persona_stats
                     (persona TEXT,
                      posts_count INTEGER,
                      avg_length INTEGER)''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️ Error initializing DB: {e}")

def log_to_grafana(success, errors, links, cost, style_stats=None, quality_score=0):
    """
    Logs metrics to SQLite database for Grafana visualization.
    """
    try:
        init_db()
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        
        # Log to publications table
        c.execute("INSERT INTO publications (timestamp, success_count, error_count, links_inserted, cost_usd, revenue_usd, quality_score) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (datetime.now(), success, errors, links, cost, style_stats.get('total_revenue', 0) if style_stats else 0, quality_score))
        
        # Log to persona_stats table
        if style_stats:
            for style, data in style_stats.items():
                if style == 'total_revenue':
                    continue
                avg_len = data['total_len'] / data['count'] if data['count'] > 0 else 0
                c.execute("INSERT INTO persona_stats (persona, posts_count, avg_length) VALUES (?, ?, ?)",
                          (style, data['count'], int(avg_len)))
        
        conn.commit()
        conn.close()
        print(f"📊 Data successfully synced to SQLite ({DB_FILE}). Quality Score: {quality_score}/100")
    except Exception as e:
        print(f"⚠️ Error writing to DB: {e}")

def fetch_affiliate_data():
    """
    Fetches real-time affiliate revenue and conversions from the Antigravity Affiliate Service.
    """
    partner_id = os.getenv("AFFILIATE_PARTNER_ID", "cb40b0df-e8a7-4448-8e76-d4709b386cdd")
    api_url = os.getenv("AFFILIATE_SERVICE_URL", "http://localhost:8087")
    
    print(f"📡 Connecting to Affiliate Service ({api_url})...")
    try:
        res = requests.get(f"{api_url}/api/partner/stats?partner_id={partner_id}", timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"⚠️ Error connecting to Affiliate Service: {e}")
    return {"balance": 0, "registrations": 0, "ftds": 0}

def calculate_dashboard_metrics(results_file='results.json', logs_file='generation_logs.jsonl'):
    print("=== PBN Executive Dashboard ===")
    
    # 1. Load Results
    if not os.path.exists(results_file):
        print(f"Error: {results_file} not found. Run publishing first.")
        return
    
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    total_tasks = len(results)
    success_count = sum(1 for r in results if r.get('status') == 'success')
    error_count = total_tasks - success_count
    link_injection_count = sum(1 for r in results if r.get('updated_old_post'))
    new_posts_count = success_count 
    
    print(f"\n[Overall Performance]")
    print(f"Total Sites: {total_tasks}")
    print(f"Successful:  {success_count} | Errors: {error_count}")
    print(f"Old Updated: {link_injection_count} | New Created: {new_posts_count}")

    # Generate execution_summary.csv
    with open('execution_summary.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Metric', 'Value', 'Description'])
        writer.writerow(['Total Sites', total_tasks, 'Total sites in batch'])
        writer.writerow(['Successful Posts', success_count, 'Published without error'])
        writer.writerow(['Errors', error_count, 'Issues (timeouts, auth)'])
        writer.writerow(['Old Posts Updated', link_injection_count, 'Links injected into existing content'])
        writer.writerow(['New Posts Created', new_posts_count, 'New pages created from scratch'])

    # 2. Analyze Styles (Persona)
    style_stats = {}
    if os.path.exists(logs_file):
        with open(logs_file, 'r') as f:
            for line in f:
                try:
                    log = json.loads(line)
                    style = log.get('style', 'unknown')
                    content_len = len(log.get('response', ''))
                    
                    if style not in style_stats:
                        style_stats[style] = {'count': 0, 'total_len': 0}
                    style_stats[style]['count'] += 1
                    style_stats[style]['total_len'] += content_len
                except:
                    continue
    else:
        # Fallback if logs don't exist (using results)
        # We can't know style from results.json unless added.
        # Assuming uniform distribution or single style for now if unknown
        pass

    # 3. Economical Metrics
    total_chars = sum(s['total_len'] for s in style_stats.values()) if style_stats else 0
    tokens = total_chars / 2 
    estimated_cost = (tokens / 1_000_000) * 0.075

    # 4. Affiliate Integration (Revenue Calculator)
    aff_data = fetch_affiliate_data()
    revenue = aff_data.get('balance', 0)
    conversions = aff_data.get('ftds', 0)
    net_profit = revenue - estimated_cost
    
    print(f"\n[Financial Performance]")
    print(f"Affiliate Revenue: ${revenue:.2f}")
    print(f"Operational Cost:  ${estimated_cost:.4f}")
    print(f"Net Profit:        ${net_profit:.2f}")
    
    # Save financial summary to CSV
    with open('financial_report.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Metric', 'Value'])
        writer.writerow(['Total Revenue', f"${revenue:.2f}"])
        writer.writerow(['Gemini Costs', f"${estimated_cost:.4f}"])
        writer.writerow(['Net Profit', f"${net_profit:.2f}"])

    print("\nCSV Reports generated.")
    
    # Calculate Quality Score
    avg_quality_score = 0
    if style_stats:
        total_score = 0
        total_items = 0
        for style, data in style_stats.items():
            avg_len = data['total_len'] / data['count']
            base_score = min(50, avg_len / 50)
            style_bonus = 30 if style == 'expert' else (20 if style == 'lifestyle' else 10)
            quality = base_score + style_bonus + 15
            total_score += (quality * data['count'])
            total_items += data['count']
        if total_items > 0:
            avg_quality_score = int(total_score / total_items)

    # Inject revenue for DB logging
    if not style_stats: style_stats = {}
    style_stats['total_revenue'] = revenue
    log_to_grafana(success_count, error_count, link_injection_count, estimated_cost, style_stats, avg_quality_score)

if __name__ == "__main__":
    calculate_dashboard_metrics()
