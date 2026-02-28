import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import datetime
import warnings

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)
try:
    from urllib3.exceptions import InsecureRequestWarning
    import requests
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
except:
    pass

# Configuration
SHEET_ID = "1CJjN_mSwrGwp2tVuaLK0vENb2c5VnYPQw0JM43HTE-c"
SHEET_TAB_NAME = "Report"
CREDENTIALS_FILE = "scraper-483621-3ae386cecfc1.json"

def get_status_emoji(status):
    status = str(status).lower()
    if "success" in status or "done" in status:
        return "✅"
    elif "error" in status or "fail" in status:
        return "❌"
    elif "pending" in status:
        return "⏳"
    else:
        return "❓"

def show_schedule():
    print(f"\n📊 Fetching Article Schedule from Google Sheets...")
    
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ Credentials file not found: {CREDENTIALS_FILE}")
        return

    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_TAB_NAME)
        
        # Manually parse headers to be safe against empty cols
        data = sheet.get_all_values()
        if not data:
            print("⚠️ Sheet is empty.")
            return

        headers = data[0]
        rows = data[1:]
        
        # Map columns
        col_date = -1
        col_topic = -1
        col_status = -1
        
        # Try finding Date or Time
        if 'Date' in headers:
            col_date = headers.index('Date')
        elif 'Time' in headers:
            col_date = headers.index('Time')
            
        # Try finding Topic
        if 'Article Topic' in headers:
            col_topic = headers.index('Article Topic')
        elif 'Topic' in headers:
            col_topic = headers.index('Topic')
            
        # Try finding Status
        if 'Status' in headers:
            col_status = headers.index('Status')
            
        if col_date == -1 or col_topic == -1 or col_status == -1:
            print(f"⚠️ Could not map required columns (Date/Time, Topic, Status). Headers found: {headers}")
            return

        published = []
        pending = []
        errors = []

        total_tasks = 0
        
        for row in rows:
            if len(row) <= col_status: continue # Skip incomplete
            
            date = row[col_date]
            topic = row[col_topic]
            status = row[col_status]
            
            if not date and not topic: continue
            
            item = {
                "date": date,
                "topic": topic,
                "status": status
            }
            
            total_tasks += 1
            
            if "success" in status.lower():
                published.append(item)
            elif "error" in status.lower():
                errors.append(item)
            else:
                pending.append(item)

        print(f"\n📈 **Summary Report**")
        print(f"Total Tasks: {total_tasks} | Published: {len(published)} | Pending: {len(pending)} | Errors: {len(errors)}")
        
        print(f"\n✅ **Recently Published** (Last 5):")
        if not published:
            print("   (No published articles yet)")
        else:
            # Show last 5
            for p in published[-5:]:
                print(f"   [{p['date']}] {p['topic']}")

        print(f"\n⏳ **Up Next / Scheduled** (Next 5):")
        if not pending:
            print("   (No pending tasks)")
        else:
            # Sort pending by date just in case
            # robust sort: pending.sort(key=lambda x: x['date']) if date format is standard
            count = 0
            today = datetime.date.today().strftime("%Y-%m-%d")
            
            for p in pending:
                if count >= 5: break
                prefix = "👉" if p['date'] == today else "  "
                print(f" {prefix} [{p['date']}] {p['topic']}")
                count += 1
                
        if errors:
            print(f"\n❌ **Errors** (Action Required):")
            for e in errors[-5:]:
                print(f"   [{e['date']}] {e['topic']} - {e['status']}")
                
        print("\n" + "="*40 + "\n")

    except Exception as e:
        print(f"⚠️ Error fetching schedule: {e}")

if __name__ == "__main__":
    show_schedule()
