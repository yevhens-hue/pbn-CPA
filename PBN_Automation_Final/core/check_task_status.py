import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

# Config
SHEET_ID = '1CJjN_mSwrGwp2tVuaLK0vENb2c5VnYPQw0JM43HTE-c'
SHEET_TAB_NAME = 'Report'
CREDS_FILE = 'scraper-483621-3ae386cecfc1.json'

def check_status():
    print("🚀 Connecting to Google Sheets...")
    
    if not os.path.exists(CREDS_FILE):
        print(f"❌ Error: {CREDS_FILE} not found!")
        return

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
    client = gspread.authorize(creds)
    
    try:
        sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_TAB_NAME)
    except gspread.exceptions.WorksheetNotFound:
        sheet = client.open_by_key(SHEET_ID).get_worksheet(0)

    # Get all values
    rows = sheet.get_all_values()
    if not rows:
        print("Sheet is empty.")
        return

    last_row = rows[-1]
    print(f"📋 Last Row Raw: {last_row}")
    
    # Assuming Status is around index 4 or 5 depending on cols
    # Let's print the last few cols
    print(f"🔍 Status Check: {last_row}")

if __name__ == "__main__":
    check_status()
