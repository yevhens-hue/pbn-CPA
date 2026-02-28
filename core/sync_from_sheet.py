import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

# Configuration
SHEET_ID = "1CJjN_mSwrGwp2tVuaLK0vENb2c5VnYPQw0JM43HTE-c"
SHEET_TAB_NAME = "Report"
CREDENTIALS_FILE = "scraper-483621-3ae386cecfc1.json"
OUTPUT_FILE = "data/sites_data.json"

def sync_data():
    print("🔄 Connecting to Google Sheets...")
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    # Adjust path if credentials are in root but script runs from core/ or root
    # We assume script is run from root PBN_Automation_Final
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ Credentials file not found: {CREDENTIALS_FILE}")
        return

    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_TAB_NAME)

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
                'Date': headers.index('Date'),
                'Site URL': headers.index('Site URL'),
                'Login': headers.index('Login'),
                'App Password': headers.index('App Password'),
                'Target Link': headers.index('Target Link'),
                'Anchor Text': headers.index('Anchor Text'),
                'Topic': headers.index('Article Topic'), # Mapped from Sheet Header
                'Author Style': headers.index('Author Style (expert/lifestyle/neutral)')
            }
        except ValueError as e:
            # Fallback for different header names if needed
            print(f"⚠️ Header mismatch: {e}. Trying alternative headers...")
            # We can print headers to debug
            print(f"Current headers: {headers}")
            return

        records = []
        for row in rows:
            if len(row) < len(headers):
                continue # Skip incomplete rows
            record = {
                'Date': row[col_map['Date']],
                'Site URL': row[col_map['Site URL']],
                'Login': row[col_map['Login']],
                'App Password': row[col_map['App Password']],
                'Target Link': row[col_map['Target Link']],
                'Anchor Text': row[col_map['Anchor Text']],
                'Topic': row[col_map['Topic']],
                'Author Style': row[col_map['Author Style']]
            }
            records.append(record)
            
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
