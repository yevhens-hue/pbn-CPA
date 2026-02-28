import requests
import time
import random
import sys
import whois
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
from dotenv import load_dotenv

load_dotenv()

# --- CONFIG ---
KEYWORDS = [
    "cricket", "ipl", "bollywood", "mumbai", "delhi", "betting", 
    "casino", "rummy", "teenpatti", "lottery", "satta", "matka",
    "news-india", "daily-update", "tech-india", "aviator", "jetx",
    "win-money", "real-cash", "app-download"
]
TLDS = [".in", ".co.in", ".com", ".net", ".org"]

SHEET_ID = "1CJjN_mSwrGwp2tVuaLK0vENb2c5VnYPQw0JM43HTE-c"
TAB_NAME = "Domains" # Make sure this tab exists!

def get_google_sheet():
    try:
        # Check for key file in parent directory or current directory or Downloads
        key_file = "scraper-483621-3ae386cecfc1.json"
        possible_paths = [
            key_file,
            f"../{key_file}",
            f"/Users/yevhen/Downloads/{key_file}"
        ]
        
        creds = None
        for path in possible_paths:
            if os.path.exists(path):
                print(f"🔑 Found credentials at: {path}")
                creds = ServiceAccountCredentials.from_json_keyfile_name(path, ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
                break
        
        if not creds:
             json_creds = os.getenv("GOOGLE_CREDENTIALS")
             if not json_creds:
                 print("⚠️ No Google Credentials found.")
                 return None
             creds_dict = json.loads(json_creds)
             creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
        
        client = gspread.authorize(creds)
        try:
            sheet = client.open_by_key(SHEET_ID).worksheet(TAB_NAME)
        except:
            print(f"⚠️ Tab '{TAB_NAME}' not found. Creating it...")
            sheet = client.open_by_key(SHEET_ID).add_worksheet(title=TAB_NAME, rows=1000, cols=5)
            sheet.append_row(["Date Found", "Domain", "Status", "Keywords Used"])
            
        return sheet
    except Exception as e:
        print(f"⚠️ Google Sheets Error: {e}")
        return None

def generate_domains(keywords, count=20):
    generated = []
    for _ in range(count):
        kw1 = random.choice(keywords)
        kw2 = random.choice(keywords)
        tld = random.choice(TLDS)
        
        variants = [
            f"{kw1}{kw2}{tld}",
            f"{kw1}-{kw2}{tld}",
            f"best{kw1}{tld}",
            f"{kw1}official{tld}",
            f"play{kw1}{tld}"
        ]
        generated.append(random.choice(variants))
    return list(set(generated))

def check_domain_availability(domain):
    try:
        w = whois.whois(domain)
        if w.domain_name is None:
            return True
        if w.expiration_date:
            if isinstance(w.expiration_date, list):
                exp_date = w.expiration_date[0]
            else:
                exp_date = w.expiration_date
            if exp_date < datetime.now():
                return True 
        return False 
    except Exception as e:
        return True

def main():
    print("🔎 Starting Domain Scanner for India Niche...")
    sheet = get_google_sheet()
    
    potential_domains = generate_domains(KEYWORDS, count=50)
    print(f"\nScanning {len(potential_domains)} generated combinations...")
    
    found_count = 0
    
    for dom in potential_domains:
        sys.stdout.write(f"Checking {dom}... ")
        sys.stdout.flush()
        
        is_free = check_domain_availability(dom)
        
        if is_free:
            print("✅ AVAILABLE!")
            found_count += 1
            if sheet:
                try:
                    sheet.append_row([
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        dom,
                        "Available",
                        "India/Gambling"
                    ])
                except Exception as e:
                    print(f"(Sheet Error: {e})")
        else:
            print("❌ Taken")
        
        time.sleep(0.5)

    print("\n" + "="*30)
    print(f"🎉 Session Finished. Found {found_count} domains.")
    print(f"📊 Results saved to Google Sheet provided.")

if __name__ == "__main__":
    main()
