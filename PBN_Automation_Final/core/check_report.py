import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv

load_dotenv()

SHEET_ID = "1CJjN_mSwrGwp2tVuaLK0vENb2c5VnYPQw0JM43HTE-c"
DEFAULT_CREDS = "scraper-483621-3ae386cecfc1.json"
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS", DEFAULT_CREDS)

def check_report():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).worksheet("Report")
    data = sheet.get_all_values()
    if data:
        print(f"Total rows in Report: {len(data)}")
        for i, row in enumerate(data[:50]):
            print(f"Row {i}: {row}")
    else:
        print("Empty Report tab.")

if __name__ == "__main__":
    check_report()
