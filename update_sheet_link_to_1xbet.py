import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
SHEET_ID = "1CJjN_mSwrGwp2tVuaLK0vENb2c5VnYPQw0JM43HTE-c"
SHEET_TAB_NAME = "Report"
CREDENTIALS_FILE = "scraper-483621-3ae386cecfc1.json"

# New Affiliate Link (with Crash deep link example)
# Format: &url=ru%2Fgames%2Fcrash
NEW_LINK = "https://refpa14435.com/L?tag=d_5300195m_1236c_&site=5300195&ad=1236&url=ru%2Fgames%2Fcrash"

def update_links():
    print("🚀 Starting Bulk Google Sheet Update to 1xBet...")
    
    # Credentials setup
    json_creds = os.getenv("GOOGLE_CREDENTIALS")
    if not json_creds:
        print("❌ Error: GOOGLE_CREDENTIALS environment variable not set.")
        return

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
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

    print("📥 Fetching all data from sheet...")
    all_values = sheet.get_all_values()
    if not all_values:
        print("ℹ️ Sheet is empty.")
        return

    header = all_values[0]
    rows = all_values[1:]
    
    # Identify key columns
    try:
        status_idx = header.index('Status')
        target_link_idx = header.index('Target Link')
    except ValueError:
        print("❌ Error: Could not find required columns ('Status' or 'Target Link').")
        return

    updated_count = 0
    
    print("🔄 Updating links for Pending tasks...")
    # Rows in gspread are 1-indexed, and we have a header, so data starts at row 2.
    for i, row in enumerate(rows, start=2):
        if len(row) > status_idx and row[status_idx].lower() == 'pending':
            print(f"📍 Updating Row {i}...")
            # Update only the specific cell for target link
            sheet.update_cell(i, target_link_idx + 1, NEW_LINK)
            updated_count += 1

    print(f"✨ Update successful! Total rows updated: {updated_count}")

if __name__ == "__main__":
    update_links()
