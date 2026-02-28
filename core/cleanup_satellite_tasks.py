import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

# Configuration
SHEET_ID = "1CJjN_mSwrGwp2tVuaLK0vENb2c5VnYPQw0JM43HTE-c"
SHEET_TAB_NAME = "Report"

def cleanup():
    print("🧹 Starting Satellite Task Cleanup...")
    
    # Credentials setup
    json_creds = os.getenv("GOOGLE_CREDENTIALS")
    creds_file = "scraper-483621-3ae386cecfc1.json"
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    if os.path.exists(creds_file):
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
    elif json_creds:
        creds_dict = json.loads(json_creds)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    else:
        print("❌ Error: No Google Credentials found.")
        return

    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_TAB_NAME)
    
    all_values = sheet.get_all_values()
    if not all_values:
        return

    header = all_values[0]
    rows = all_values[1:]
    
    # Identify indices
    try:
        site_url_idx = header.index('Site URL')
        topic_idx = header.index('Article Topic')
    except ValueError:
        try:
            site_url_idx = 1 # Fallback to standard Column B
            topic_idx = 6    # Fallback to standard Column G
        except:
             print("❌ Error: Could not determine column structure.")
             return

    rows_to_keep = [header]
    removed_count = 0
    
    for row in rows:
        if len(row) <= max(site_url_idx, topic_idx):
            rows_to_keep.append(row)
            continue
            
        site_url = row[site_url_idx].lower()
        topic = row[topic_idx]
        
        # Criteria for removal: satellite domains or "Template (Fallback)"
        is_satellite = "satellite1.com" in site_url or "finance-blog-test.com" in site_url
        is_fallback = "Template (Fallback)" in topic
        
        if is_satellite or is_fallback:
            print(f"🗑️ Removing: {site_url} | {topic}")
            removed_count += 1
            continue
            
        rows_to_keep.append(row)

    if removed_count > 0:
        print(f"✅ Found {removed_count} rows to remove. Updating sheet...")
        sheet.clear()
        sheet.update('A1', rows_to_keep)
        print("✨ Cleanup successful!")
    else:
        print("ℹ️ No satellite tasks or fallbacks found.")

if __name__ == "__main__":
    cleanup()
