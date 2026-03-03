#!/usr/bin/env python3
"""
Smart Task Scheduler — Adds diverse topics from content_plan_india.json
to the Google Sheet for the next N days.

Uses the full 50-topic content plan instead of hardcoded Aviator topics.
Checks which topics are already published/scheduled and only adds NEW ones.

Usage:
  python3 add_tasks_to_sheet.py              # Add 14 days of tasks
  python3 add_tasks_to_sheet.py --days 7     # Add 7 days of tasks
"""

import gspread
import json
import datetime
import random
import sys
import os
from collections import defaultdict
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()

# Configuration
SHEET_ID = "1CJjN_mSwrGwp2tVuaLK0vENb2c5VnYPQw0JM43HTE-c"
SHEET_TAB_NAME = "Report"
CONTENT_PLAN_FILE = "data/content_plan_india.json"

# Site Data
SITE_URL = "https://luckybetvip.com"
LOGIN = "admin"
APP_PASSWORD = "4SvP8Q4hqfxnsDo6xS351Xcr"
TARGET_LINK = "https://refpa14435.com/L?tag=d_5300195m_1236c_&site=5300195&ad=1236&url=ru%2Fgames%2Fcrash"

# Style rotation for variety
STYLES = ["expert", "lifestyle", "neutral"]

def load_content_plan():
    """Load diverse topics from content_plan_india.json."""
    paths = [CONTENT_PLAN_FILE, f"../{CONTENT_PLAN_FILE}", f"PBN_Automation_Final/{CONTENT_PLAN_FILE}"]
    for p in paths:
        if os.path.exists(p):
            with open(p) as f:
                data = json.load(f)
                return data.get("topics", [])
    print(f"❌ Content plan not found: {CONTENT_PLAN_FILE}")
    return []

def get_used_topics_from_sheet(sheet):
    """Get list of topics already in the sheet (published or scheduled)."""
    all_values = sheet.get_all_values()
    used = set()
    for row in all_values[1:]:  # Skip header
        if len(row) > 6:
            topic = row[6].strip()  # Column G = Article Topic
            if topic:
                used.add(topic.lower())
    return used

def get_google_creds():
    """Get Google credentials from env or file."""
    json_creds = os.getenv("GOOGLE_CREDENTIALS")
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    if json_creds:
        if os.path.exists(json_creds):
            return ServiceAccountCredentials.from_json_keyfile_name(json_creds, scope)
        else:
            try:
                creds_dict = json.loads(json_creds)
                return ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            except:
                pass
    
    # Fallback to local file
    for f in ['scraper-483621-3ae386cecfc1.json', '../scraper-483621-3ae386cecfc1.json']:
        if os.path.exists(f):
            return ServiceAccountCredentials.from_json_keyfile_name(f, scope)
    
    print("❌ No Google credentials found.")
    return None

def add_tasks_to_sheet():
    # Parse --days flag
    num_days = 14
    if "--days" in sys.argv:
        try:
            idx = sys.argv.index("--days")
            num_days = int(sys.argv[idx + 1])
        except (IndexError, ValueError):
            pass
    
    # Load content plan
    topics = load_content_plan()
    if not topics:
        return
    
    # Connect to Google Sheets
    creds = get_google_creds()
    if not creds:
        return
    
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_TAB_NAME)
    
    # Get already-used topics
    used_topics = get_used_topics_from_sheet(sheet)
    print(f"📊 Found {len(used_topics)} existing topics in sheet.")
    
    # Filter to unused topics
    available = [t for t in topics if t['title'].lower() not in used_topics]
    print(f"📋 Available unused topics: {len(available)} out of {len(topics)}")
    
    if not available:
        print("⚠️ All topics have been used! Consider adding new topics to content_plan_india.json.")
        return
    
    # Shuffle for variety (mix categories)
    random.shuffle(available)
    
    # Generate tasks: 2 articles per day
    today = datetime.date.today()
    rows_to_append = []
    topic_idx = 0
    
    # Distribute topics across categories for balance
    categories = defaultdict(list)
    for t in available:
        categories[t.get('category', 'General')].append(t)
    
    # Round-robin across categories
    cat_keys = list(categories.keys())
    random.shuffle(cat_keys)
    balanced_topics = []
    while any(categories[k] for k in cat_keys):
        for k in cat_keys:
            if categories[k]:
                balanced_topics.append(categories[k].pop(0))
    
    articles_per_day = 2
    total_needed = num_days * articles_per_day
    selected_topics = balanced_topics[:total_needed]
    
    for i, topic_data in enumerate(selected_topics):
        day_offset = i // articles_per_day
        task_date = (today + datetime.timedelta(days=day_offset)).strftime("%Y-%m-%d")
        style = STYLES[i % len(STYLES)]
        
        # Generate anchor text from keyword
        anchor = topic_data.get('keyword', topic_data['title'].lower()[:30])
        
        row = [
            task_date,           # Time/Date
            SITE_URL,            # Site URL
            LOGIN,               # Login
            APP_PASSWORD,        # App Password
            TARGET_LINK,         # Target Link
            anchor,              # Anchor Text
            topic_data['title'], # Article Topic
            style,               # Author Style
            "Pending"            # Status
        ]
        rows_to_append.append(row)
    
    if rows_to_append:
        sheet.append_rows(rows_to_append)
        print(f"\n✅ Successfully added {len(rows_to_append)} tasks for {num_days} days!")
        print(f"   📅 Schedule: {today.strftime('%Y-%m-%d')} → {(today + datetime.timedelta(days=num_days-1)).strftime('%Y-%m-%d')}")
        print(f"   📝 Topics per day: {articles_per_day}")
        
        # Show category distribution
        cat_count = defaultdict(int)
        for t in selected_topics:
            cat_count[t.get('category', 'General')] += 1
        print(f"\n   Category distribution:")
        for cat, count in sorted(cat_count.items(), key=lambda x: -x[1]):
            print(f"   • {cat}: {count} articles")
    else:
        print("ℹ️ No new tasks to add.")

if __name__ == "__main__":
    add_tasks_to_sheet()
