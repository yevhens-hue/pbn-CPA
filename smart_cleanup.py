import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

# Configuration
SHEET_ID = "1CJjN_mSwrGwp2tVuaLK0vENb2c5VnYPQw0JM43HTE-c"
SHEET_TAB_NAME = "Report"
CREDENTIALS_FILE = "scraper-483621-3ae386cecfc1.json"

# Bogus items to remove
BOGUS_STRINGS = ["satellite1.com", "finance-blog-test.com", "Template (Fallback)"]

def smart_cleanup():
    print(" sweep Starting Smart Google Sheet Cleanup...")
    
    # Credentials setup
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ Error: Credentials file {CREDENTIALS_FILE} not found.")
        return

    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_TAB_NAME)

    print("📥 Fetching all data from sheet...")
    all_values = sheet.get_all_values()
    if not all_values:
        print("ℹ️ Sheet is empty.")
        return

    header = all_values[0]
    rows = all_values[1:]
    
    # Identify key columns
    try:
        site_url_idx = header.index('Site URL')
        topic_idx = header.index('Article Topic')
    except ValueError:
        print("❌ Error: Could not find required columns.")
        return

    rows_to_keep = [header]
    removed_count = 0
    
    print("🔍 Filtering rows...")
    for row in rows:
        # 1. Skip if row is basically empty
        if len(row) < 3 or not any(cell.strip() for cell in row):
            removed_count += 1
            continue
            
        site_url = row[site_url_idx].lower() if len(row) > site_url_idx else ""
        topic = row[topic_idx] if len(row) > topic_idx else ""
        
        # 2. Check for bogus domains OR placeholder topics
        is_bogus = any(s.lower() in site_url or s.lower() in topic.lower() for s in BOGUS_STRINGS)
        
        # 3. Check for specific "Generation Failed" or error entries that are NOT real tasks
        # (Be careful here - don't delete real failures the user might want to see)
        # For now, let's stick to the user's request: ghost sites.
        
        if is_bogus:
            print(f"🗑️ Removing: {site_url} | {topic[:30]}...")
            removed_count += 1
            continue
            
        rows_to_keep.append(row)

    if removed_count > 0:
        print(f"✅ Found {removed_count} bogus/empty rows to remove. Updating sheet...")
        sheet.clear()
        # Use update_rows or similar if possible, but clear/update is safe for total refreshes
        sheet.update('A1', rows_to_keep)
        print(f"✨ Cleanup successful! Remaining rows: {len(rows_to_keep)}")
    else:
        print("ℹ️ No bogus domains or empty rows found.")

if __name__ == "__main__":
    smart_cleanup()
