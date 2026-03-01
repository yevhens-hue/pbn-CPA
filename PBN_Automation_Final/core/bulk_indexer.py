#!/usr/bin/env python3
import os
import json
import gspread
import datetime
import time
from oauth2client.service_account import ServiceAccountCredentials
try:
    from core.indexing_api import submit_to_google_indexing
except ImportError:
    from indexing_api import submit_to_google_indexing

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- CONFIG ---
SHEET_ID = "1CJjN_mSwrGwp2tVuaLK0vENb2c5VnYPQw0JM43HTE-c"
SHEET_TAB_NAME = "Report"

def bulk_index_from_sheet():
    """
    Fetches all published links from the Google Sheet and submits them to the Indexing API.
    """
    try:
        json_creds = os.getenv("GOOGLE_CREDENTIALS")
        if not json_creds:
            print("❌ Error: GOOGLE_CREDENTIALS environment variable missing.")
            return

        # Handle case where GOOGLE_CREDENTIALS is a filename instead of a JSON string
        if json_creds.endswith('.json') and os.path.exists(json_creds):
            with open(json_creds, 'r') as f:
                creds_dict = json.load(f)
        elif os.path.exists(os.path.join("PBN_Automation_Final", json_creds)):
             with open(os.path.join("PBN_Automation_Final", json_creds), 'r') as f:
                creds_dict = json.load(f)
        else:
            try:
                creds_dict = json.loads(json_creds)
            except json.JSONDecodeError:
                print(f"❌ Error: GOOGLE_CREDENTIALS is neither a valid JSON string nor a found file: {json_creds}")
                return

        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)

        # Open Sheet
        try:
            sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_TAB_NAME)
        except gspread.exceptions.WorksheetNotFound:
            print(f"⚠️ Worksheet '{SHEET_TAB_NAME}' not found. Using first sheet.")
            sheet = client.open_by_key(SHEET_ID).sheet1

        records = sheet.get_all_records()
        if not records:
            print("ℹ️ Sheet is empty.")
            return

        headers = records[0].keys()
        print(f"🔍 Detected headers: {list(headers)}")

        indexed_count = 0
        for i, record in enumerate(records):
            # Flexible Link/URL detection
            link = None
            for key in ['Post URL', 'Link', 'Post Link', 'Url', 'URL', 'post_link', 'New Post URL']:
                if record.get(key):
                    link = record.get(key)
                    break
            
            # Flexible status detection
            raw_status = ""
            for key in ['Status', 'status', 'Result']:
                if record.get(key):
                    raw_status = str(record.get(key)).lower()
                    break

            # Check if 'success' is anywhere in the status (handles "✅ Success")
            is_success = 'success' in raw_status

            if link and str(link).startswith('http') and is_success:
                print(f"🚀 [{i+1}] Submitting URL: {link}")
                success = submit_to_google_indexing(link)
                if success:
                    indexed_count += 1
                # Respect Google Indexing API quotas/limits (standard is 200/day)
                time.sleep(1) 
            elif link and str(link).startswith('http'):
                print(f"⏩ [{i+1}] Skipping URL (Status not success): {link} | Status: {raw_status}")
            else:
                 # Debug: print if link is missing or malformed
                 if i < 5: # Only first 5 for sanity
                     print(f"❓ [{i+1}] Invalid/Missing Link: {link} | Status: {raw_status} | Keys: {record.keys()}")

        print(f"✅ Bulk indexing complete. {indexed_count} URLs submitted.")

    except Exception as e:
        print(f"❌ Bulk Indexer Error: {e}")

if __name__ == "__main__":
    bulk_index_from_sheet()
