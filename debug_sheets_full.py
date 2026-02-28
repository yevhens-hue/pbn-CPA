import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Config
SHEET_ID = '1CJjN_mSwrGwp2tVuaLK0vENb2c5VnYPQw0JM43HTE-c'
SHEET_TAB_NAME = 'Report'
CREDS_FILE = 'scraper-483621-3ae386cecfc1.json'

def debug_sheet():
    json_creds = os.getenv("GOOGLE_CREDENTIALS")
    if not json_creds:
        print("❌ Error: GOOGLE_CREDENTIALS environment variable not set.")
        return

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    if os.path.exists(json_creds):
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_creds, scope)
    else:
        try:
            import json as _json
            creds_dict = _json.loads(json_creds)
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        except Exception as e:
            print(f"❌ Error parsing GOOGLE_CREDENTIALS: {e}")
            return

    client = gspread.authorize(creds)
    
    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_TAB_NAME)
    
    # Get header row
    headers = sheet.row_values(1)
    print(f"📋 Headers: {headers}")
    
    # Check for duplicates or empty headers
    seen = set()
    dupes = []
    for h in headers:
        if h in seen:
            dupes.append(h)
        seen.add(h)
    
    if dupes:
        print(f"❌ Found duplicate headers: {dupes}")
    
    # Get all values
    all_values = sheet.get_all_values()
    
    # Search for specific topic
    search_term = "Cricket Betting Tips"
    found = False
    print(f"\n🔍 Searching for '{search_term}':")
    for i, row in enumerate(all_values):
        if any(search_term in str(cell) for cell in row):
            print(f"✅ Found in Row {i+1}: {row}")
            found = True
    
    if not found:
        print(f"❌ Topic '{search_term}' not found in the sheet.")

if __name__ == "__main__":
    debug_sheet()
