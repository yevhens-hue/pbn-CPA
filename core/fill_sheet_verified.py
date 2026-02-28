import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import os

# Config
SHEET_ID = '1CJjN_mSwrGwp2tVuaLK0vENb2c5VnYPQw0JM43HTE-c'
SHEET_TAB_NAME = 'Report'
CREDS_FILE = 'scraper-483621-3ae386cecfc1.json'

def fill_sheet():
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
        print(f"⚠️ Worksheet '{SHEET_TAB_NAME}' not found, trying first sheet...")
        sheet = client.open_by_key(SHEET_ID).get_worksheet(0)

    # Headers structure verification
    headers = sheet.row_values(1)
    print(f"📋 Headers found: {headers}")

    # Row Data (Minimalist approach to test fallback + HTTPS)
    # Columns: Time, Site URL, Login, App Password, Target Link, Anchor Text, Topic, Style, Status
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_row = [
        timestamp,
        "https://luckybetvip.com/",  # Site URL (Explicitly HTTPS)
        "",                          # Login (Will be fetched from json)
        "",                          # Password (Will be fetched from json)
        "",                          # Target Link (Will be fetched from json)
        "",                          # Anchor (Will be fetched from json)
        "Aviator Game Hints & Tricks 2026", # Topic
        "expert",                    # Style
        "Pending"                    # Status
    ]

    print(f"📝 Appending row: {new_row}")
    sheet.append_row(new_row)
    print("✅ Successfully added task to Sheet!")

if __name__ == "__main__":
    fill_sheet()
