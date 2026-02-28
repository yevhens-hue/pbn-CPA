import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# Configuration
SHEET_ID = "1CJjN_mSwrGwp2tVuaLK0vENb2c5VnYPQw0JM43HTE-c"
SHEET_TAB_NAME = "Report" # Tasks are read from here
CREDENTIALS_FILE = "scraper-483621-3ae386cecfc1.json"

# Site Data
SITE_URL = "https://luckybetvip.com"
LOGIN = "admin"
APP_PASSWORD = "4SvP8Q4hqfxnsDo6xS351Xcr" # From sites_data.json
TARGET_LINK = "https://1win.com/reg"

# 10 Tasks to Add (Diverse Topics & Anchors)
# Get today's date
today = datetime.date.today()

tasks = [
    {
        "Date": (today + datetime.timedelta(days=0)).strftime("%Y-%m-%d"),
        "Site URL": SITE_URL,
        "Topic": "Aviator Game Tricks 2026: Proven Winning Methods",
        "Target Link": TARGET_LINK,
        "Anchor Text": "aviator tricks",
        "Status": "Pending",
        "Login": LOGIN,
        "App Password": APP_PASSWORD,
        "Author Style": "expert"
    },
    {
        "Date": (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
        "Site URL": SITE_URL,
        "Topic": "Best Time to Play Aviator in India for Max Profit",
        "Target Link": TARGET_LINK,
        "Anchor Text": "best time to play aviator",
        "Status": "Pending",
        "Login": LOGIN,
        "App Password": APP_PASSWORD,
        "Author Style": "lifestyle" # Change style for variety
    },
    {
        "Date": (today + datetime.timedelta(days=2)).strftime("%Y-%m-%d"),
        "Site URL": SITE_URL,
        "Topic": "Aviator Signals Telegram Groups Review: Scam or Legit?",
        "Target Link": TARGET_LINK,
        "Anchor Text": "aviator signals",
        "Status": "Pending",
        "Login": LOGIN,
        "App Password": APP_PASSWORD,
        "Author Style": "neutral"
    },
    {
        "Date": (today + datetime.timedelta(days=3)).strftime("%Y-%m-%d"),
        "Site URL": SITE_URL,
        "Topic": "1win Aviator Promo Code 2026 for New Players",
        "Target Link": TARGET_LINK,
        "Anchor Text": "1win promo code", # Different anchor
        "Status": "Pending",
        "Login": LOGIN,
        "App Password": APP_PASSWORD,
        "Author Style": "expert"
    },
    {
        "Date": (today + datetime.timedelta(days=4)).strftime("%Y-%m-%d"),
        "Site URL": SITE_URL,
        "Topic": "How to Withdraw Money from Aviator (Paytm/UPI Guide)",
        "Target Link": TARGET_LINK,
        "Anchor Text": "withdraw money from aviator",
        "Status": "Pending",
        "Login": LOGIN,
        "App Password": APP_PASSWORD,
        "Author Style": "neutral"
    },
    {
        "Date": (today + datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
        "Site URL": SITE_URL,
        "Topic": "Aviator Prediction App APK Download: Is It Safe?",
        "Target Link": TARGET_LINK,
        "Anchor Text": "aviator predictor",
        "Status": "Pending",
        "Login": LOGIN,
        "App Password": APP_PASSWORD,
        "Author Style": "technical" # Use technical style if possible, defaults to expert
    },
    {
        "Date": (today + datetime.timedelta(days=6)).strftime("%Y-%m-%d"),
        "Site URL": SITE_URL,
        "Topic": "Low Risk Aviator Strategy for Beginners (x1.20 Method)",
        "Target Link": TARGET_LINK,
        "Anchor Text": "low risk strategy",
        "Status": "Pending",
        "Login": LOGIN,
        "App Password": APP_PASSWORD,
        "Author Style": "expert"
    },
    {
        "Date": (today + datetime.timedelta(days=7)).strftime("%Y-%m-%d"),
        "Site URL": SITE_URL,
        "Topic": "Aviator Auto-Cashout Settings Guide for Consistent Wins",
        "Target Link": TARGET_LINK,
        "Anchor Text": "auto cashout settings",
        "Status": "Pending",
        "Login": LOGIN,
        "App Password": APP_PASSWORD,
        "Author Style": "expert"
    },
    {
        "Date": (today + datetime.timedelta(days=8)).strftime("%Y-%m-%d"),
        "Site URL": SITE_URL,
        "Topic": "Biggest Aviator Wins in India 2026: Success Stories",
        "Target Link": TARGET_LINK,
        "Anchor Text": "big wins aviator",
        "Status": "Pending",
        "Login": LOGIN,
        "App Password": APP_PASSWORD,
        "Author Style": "lifestyle"
    },
    {
        "Date": (today + datetime.timedelta(days=9)).strftime("%Y-%m-%d"),
        "Site URL": SITE_URL,
        "Topic": "Is Aviator Legal in India? Real Money Gaming Laws 2026",
        "Target Link": TARGET_LINK,
        "Anchor Text": "is aviator legal",
        "Status": "Pending",
        "Login": LOGIN,
        "App Password": APP_PASSWORD,
        "Author Style": "neutral"
    }
]

def add_tasks_to_sheet():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_TAB_NAME)

    # Prepare rows to append based on sheet header order
    # Assuming columns are: Date, Site URL, Topic, Target Link, Anchor Text, Status, Login, App Password, Author Style
    # We will just append rows matching this structure.
    
    rows_to_append = []
    for task in tasks:
        row = [
            task["Date"],
            task["Site URL"],
            task["Login"],
            task["App Password"],
            task["Target Link"],
            task["Anchor Text"],
            task["Topic"],
            task["Author Style"],
            task["Status"]
        ]
        rows_to_append.append(row)

    sheet.append_rows(rows_to_append)
    print(f"Successfully added {len(rows_to_append)} tasks to the sheet.")

if __name__ == "__main__":
    add_tasks_to_sheet()
