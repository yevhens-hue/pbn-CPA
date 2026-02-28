#!/usr/bin/env python3
"""
Sheet Cleaner — видаляє рядки з помилками, додає правильні заголовки,
та прибирає зайві порожні рядки з Google Sheet.
"""

import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
SPREADSHEET_ID = '1CJjN_mSwrGwp2tVuaLK0vENb2c5VnYPQw0JM43HTE-c'
SHEET_GID = 40823346

# Correct headers for the sheet
CLEAN_HEADERS = [
    'Time', 'Site URL', 'Login', 'App Password',
    'Target Link', 'Anchor Text', 'Article Topic',
    'Author Style', 'Status', 'Post URL', 'Model Used'
]

def get_sheet():
    creds_raw = os.getenv('GOOGLE_CREDENTIALS', '')
    if creds_raw.endswith('.json') and os.path.exists(creds_raw):
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_raw, SCOPE)
    else:
        creds_dict = json.loads(creds_raw) if creds_raw.startswith('{') else None
        if creds_dict:
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
        else:
            creds = ServiceAccountCredentials.from_json_keyfile_name(creds_raw, SCOPE)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    # Find exact worksheet by gid
    for ws in spreadsheet.worksheets():
        if ws.id == SHEET_GID:
            return ws
    return spreadsheet.sheet1

def clean_sheet():
    print("🔗 Connecting to Google Sheet...")
    sheet = get_sheet()
    all_values = sheet.get_all_values()
    
    if not all_values:
        print("❌ Sheet is empty.")
        return

    print(f"📊 Found {len(all_values)} rows total")
    
    # --- 1. Set correct headers in row 1 ---
    print("📝 Setting correct headers...")
    sheet.update('A1:K1', [CLEAN_HEADERS])
    
    # --- 2. Find and delete error rows (keeping headers + success/pending) ---
    rows_to_delete = []
    for i, row in enumerate(all_values[1:], start=2):  # skip header row
        status = row[8].strip() if len(row) > 8 else ''
        topic = row[6].strip() if len(row) > 6 else ''
        site_url = row[1].strip() if len(row) > 1 else ''
        
        # Normalize status — remove emoji and lowercase
        status_clean = status.replace('❌', '').replace('✅', '').replace('⏳', '').strip().lower()
        
        # Delete if: error status, or completely empty row, or garbage template row
        if status_clean in ['error', 'generation failed', 'failed']:
            rows_to_delete.append(i)
            print(f"   ❌ Deleting error row {i}: '{topic}'")
        elif not site_url and not topic:
            rows_to_delete.append(i)
            print(f"   🗑️ Deleting empty row {i}")
        elif topic in ['Template (Fallback)', 'template (fallback)'] and not site_url:
            rows_to_delete.append(i)
            print(f"   🗑️ Deleting garbage template row {i}")
    
    # Delete in reverse order to preserve row numbers
    for row_idx in sorted(rows_to_delete, reverse=True):
        sheet.delete_rows(row_idx)
        print(f"   ✅ Deleted row {row_idx}")
    
    # --- 3. Report final state ---
    final_values = sheet.get_all_values()
    total = len(final_values) - 1  # minus header
    success = sum(1 for r in final_values[1:] if len(r) > 8 and 'success' in r[8].lower())
    pending = sum(1 for r in final_values[1:] if len(r) > 8 and 'pending' in r[8].lower())
    
    print(f"\n✅ Sheet cleaned!")
    print(f"   📋 Total tasks: {total}")
    print(f"   ✅ Success: {success}")
    print(f"   ⏳ Pending: {pending}")
    print(f"   🗑️ Deleted: {len(rows_to_delete)} rows")

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    clean_sheet()
