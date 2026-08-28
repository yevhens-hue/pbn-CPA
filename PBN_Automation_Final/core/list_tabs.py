import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv

load_dotenv()

SHEET_ID = "1CJjN_mSwrGwp2tVuaLK0vENb2c5VnYPQw0JM43HTE-c"
DEFAULT_CREDS = "scraper-483621-3ae386cecfc1.json"
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS", DEFAULT_CREDS)

def list_tabs():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(SHEET_ID)
    worksheets = spreadsheet.worksheets()
    print("Available tabs:")
    for ws in worksheets:
        print(f"- {ws.title}")

if __name__ == "__main__":
    list_tabs()
