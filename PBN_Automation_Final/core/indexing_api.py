#!/usr/bin/env python3
import requests
import os
import json
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# --- CONFIG ---
# Use the existing credentials file
CREDENTIALS_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "scraper-483621-3ae386cecfc1.json")
INDEXING_SCOPE = ["https://www.googleapis.com/auth/indexing"]

def submit_to_google_indexing(url, type="URL_UPDATED"):
    """
    Notifies Google Indexing API about a new or updated URL.
    types: 'URL_UPDATED' or 'URL_DELETED'
    """
    try:
        json_creds = os.getenv("GOOGLE_CREDENTIALS")
        if json_creds:
            if os.path.exists(json_creds):
                credentials = service_account.Credentials.from_service_account_file(json_creds, scopes=INDEXING_SCOPE)
            else:
                creds_dict = json.loads(json_creds)
                credentials = service_account.Credentials.from_service_account_info(creds_dict, scopes=INDEXING_SCOPE)
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                 print(f"⚠️ Indexing API: Credentials file not found at {CREDENTIALS_FILE} and GOOGLE_CREDENTIALS not set.")
                 return False
            credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=INDEXING_SCOPE)

        
        # Refresh token
        credentials.refresh(Request())
        token = credentials.token

        endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        payload = {
            "url": url,
            "type": type
        }

        response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ Indexing API: Successfully notified Google about {url}")
            return True
        else:
            print(f"❌ Indexing API: Error {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Indexing API Exception: {e}")
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        submit_to_google_indexing(sys.argv[1])
    else:
        print("Usage: python3 indexing_api.py <URL>")
