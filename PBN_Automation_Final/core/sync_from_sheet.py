import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

# Configuration
SHEET_ID = "1CJjN_mSwrGwp2tVuaLK0vENb2c5VnYPQw0JM43HTE-c"
SHEET_TAB_NAME = "Report"
DEFAULT_CREDS = "scraper-483621-3ae386cecfc1.json"
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS", DEFAULT_CREDS)
OUTPUT_FILE = "data/sites_data.json"

def sync_data():
    from dotenv import load_dotenv
    load_dotenv()
    
    global CREDENTIALS_FILE
    CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS", DEFAULT_CREDS)

    print(f"🔄 Connecting to Google Sheets using {CREDENTIALS_FILE}...")
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ Credentials file not found: {CREDENTIALS_FILE}")
        return

    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_TAB_NAME)
    except Exception as e:
        print(f"❌ Error connecting to sheet: {e}")
        return

    print("📥 Fetching all records...")
    # get_all_records uses the first row as keys. 
    # Ensure the header names match what we expect or we map them.
    # Headers in add_tasks_to_sheet.py were: Date, Site URL, Login, App Password, Target Link, Anchor Text, Topic, Author Style, Status
    expected_headers = ['Date', 'Site URL', 'Login', 'App Password', 'Target Link', 'Anchor Text', 'Article Topic', 'Author Style', 'Status']
    
    # Try fetching with expected headers first to filter out empty cols
    try:
        # Note: gspread get_all_records blindly pulls all data. If there are extra empty columns, it fails on duplicate empty headers.
        # We should use get_all_values() and map manually to be safe.
        data = sheet.get_all_values()
        headers = data[0]
        rows = data[1:]
        
        # Find indices of required columns
        try:
            col_map = {
                'Site URL': headers.index('Site URL'),
                'Login': headers.index('Login'),
                'App Password': headers.index('App Password'),
                'Target Link': headers.index('Target Link'),
                'Anchor Text': headers.index('Anchor Text'),
                'Topic': headers.index('Article Topic'),
                'Author Style': headers.index('Author Style')
            }
        except ValueError as e:
            print(f"⚠️ Header mismatch: {e}. Trying fuzzy match...")
            # Fuzzy match or fallback
            col_map = {}
            for target in ['Site URL', 'Login', 'App Password', 'Target Link', 'Anchor Text']:
                try: col_map[target] = headers.index(target)
                except: pass
            
            # Special cases for topic and style
            for h in headers:
                if 'Topic' in h: col_map['Topic'] = headers.index(h)
                if 'Author Style' in h: col_map['Author Style'] = headers.index(h)

        records = []
        seen_sites = set()
        for row in rows:
            if len(row) < 5: continue
            
            site_url = row[col_map.get('Site URL', 0)].strip()
            login = row[col_map.get('Login', 1)].strip()
            password = row[col_map.get('App Password', 2)].strip()
            
            if not site_url or not login or not password:
                continue
            
            if site_url in seen_sites:
                continue
                
            record = {
                'site_url': site_url,
                'login': login,
                'app_password': password,
                'target_url': row[col_map.get('Target Link', 3)].strip(),
                'anchor': row[col_map.get('Anchor Text', 4)].strip(),
                'topic': row[col_map.get('Topic', 5)].strip(),
                'author_style': row[col_map.get('Author Style', 6)].strip()
            }
            if record['site_url'].startswith('http'):
                records.append(record)
                seen_sites.add(site_url)
            
        sites_data = records

    except Exception as e:
        print(f"❌ Error parsing sheet manually: {e}")
        return

    print(f"💾 Saving {len(sites_data)} tasks to {OUTPUT_FILE}...")
    
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(sites_data, f, indent=2, ensure_ascii=False)
        
    print("✅ Sync Complete!")

if __name__ == "__main__":
    sync_data()
