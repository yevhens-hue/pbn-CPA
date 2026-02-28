import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

# Configuration
SHEET_ID = "1CJjN_mSwrGwp2tVuaLK0vENb2c5VnYPQw0JM43HTE-c"
CREDS_FILE = "scraper-483621-3ae386cecfc1.json"

def check_sheets():
    if not os.path.exists(CREDS_FILE):
        print(f"❌ Credentials file not found: {CREDS_FILE}")
        return

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
    client = gspread.authorize(creds)

    try:
        sheet = client.open_by_key(SHEET_ID)
        print(f"📄 Sheet Title: {sheet.title}")
        print("-" * 30)
        
        for worksheet in sheet.worksheets():
            print(f"📑 Tab: '{worksheet.title}' (ID: {worksheet.id})")
            try:
                headers = worksheet.row_values(1)
                print(f"   Headers: {headers}")
            except Exception as e:
                print(f"   ⚠️ Could not read headers: {e}")
            print("-" * 30)
            
    except Exception as e:
        print(f"❌ Error opening sheet: {e}")

if __name__ == "__main__":
    check_sheets()
