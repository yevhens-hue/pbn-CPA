import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

# --- CONFIG ---
SERVICE_ACCOUNT_FILE = 'gsc_credentials.json' # Needs to be created by user
SITE_URL = "https://luckybetvip.com/" # MUST include trailing slash for GSC

def get_gsc_service():
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"❌ Error: {SERVICE_ACCOUNT_FILE} not found. Please follow instructions to create it.")
        return None
    
    scopes = ['https://www.googleapis.com/auth/webmasters.readonly']
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    return build('searchconsole', 'v1', credentials=creds)

def fetch_top_keywords(days=30, limit=10):
    service = get_gsc_service()
    if not service: return []

    request = {
        'startDate': '2026-01-22', # Example dates, should be dynamic
        'endDate': '2026-02-21',
        'dimensions': ['query'],
        'rowLimit': limit
    }
    
    try:
        response = service.searchAnalytics().query(siteUrl=SITE_URL, body=request).execute()
        rows = response.get('rows', [])
        print(f"✅ Fetched {len(rows)} keywords from GSC.")
        return rows
    except Exception as e:
        print(f"❌ GSC API Error: {e}")
        return []

if __name__ == "__main__":
    # Test fetch
    keywords = fetch_top_keywords()
    for kw in keywords:
        print(f"- {kw['keys'][0]}: {kw['clicks']} clicks, {kw['impressions']} impressions")
