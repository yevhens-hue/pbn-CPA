import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
import datetime

SHEET_ID = "1CJjN_mSwrGwp2tVuaLK0vENb2c5VnYPQw0JM43HTE-c"
SHEET_TAB_NAME = "Report"
CREDENTIALS_FILE = "scraper-483621-3ae386cecfc1.json"
SITES_DATA = "../sites_data.json"

CLEAN_HEADERS = [
    'Time', 'Site URL', 'Login', 'App Password',
    'Target Link', 'Anchor Text', 'Article Topic',
    'Author Style', 'Status', 'Post URL', 'Model Used'
]

def load_sites_data():
    if not os.path.exists(SITES_DATA):
        print(f"❌ Could not find {SITES_DATA}")
        return []
    with open(SITES_DATA, 'r') as f:
        return json.load(f)

def reset_sheet():
    print("🚀 Connecting to Google Sheets...")
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_TAB_NAME)

    print("🧹 Clearing entire sheet...")
    sheet.clear()

    print("📝 Re-writing clean headers...")
    sheet.update('A1:K1', [CLEAN_HEADERS])

    sites = load_sites_data()
    if not sites:
        return

    print(f"📥 Generating {len(sites)} new tasks based on sites_data.json...")
    today = datetime.date.today()
    rows_to_append = []

    for i, site in enumerate(sites):
        row = [
            (today + datetime.timedelta(days=i)).strftime("%Y-%m-%d"),
            site.get("site_url", ""),
            site.get("login", ""),
            site.get("app_password", ""),
            site.get("target_url", ""),
            site.get("anchor", ""),
            site.get("topic", ""),
            site.get("author_style", "expert"),
            "Pending",
            "",
            ""
        ]
        rows_to_append.append(row)

    if rows_to_append:
        sheet.append_rows(rows_to_append)
        print(f"✅ Successfully added {len(rows_to_append)} perfectly clean tasks to the sheet.")

if __name__ == "__main__":
    reset_sheet()
