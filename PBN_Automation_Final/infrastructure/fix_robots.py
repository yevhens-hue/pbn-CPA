#!/usr/bin/env python3
import requests
import base64
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Config
SITE_URL = "https://luckybetvip.com"
LOGIN = "admin"
APP_PASSWORD = "4SvP8Q4hqfxnsDo6xS351Xcr"

def get_auth_headers():
    token = base64.b64encode(f"{LOGIN}:{APP_PASSWORD}".encode()).decode()
    return {
        'Authorization': f'Basic {token}',
        'Content-Type': 'application/json'
    }

def check_robots():
    print(f"🔍 Checking robots.txt for {SITE_URL}...")
    try:
        r = requests.get(f"{SITE_URL}/robots.txt", timeout=10)
        print("Current robots.txt content:")
        print("-" * 30)
        print(r.text)
        print("-" * 30)
        return r.text
    except Exception as e:
        print(f"❌ Error checking robots: {e}")
        return None

def main():
    content = check_robots()
    if not content:
        return

    if "http://luckybetvip.com" in content:
        print("⚠️ Found insecure HTTP sitemap link!")
        new_content = content.replace("http://luckybetvip.com", "https://luckybetvip.com")
        
        print("\n🚀 Attempting to update robots.txt via Yoast/WP REST API (if possible)...")
        # Note: Standard WP REST API doesn't allow direct robots.txt edits. 
        # This usually requires a specific plugin endpoint or file access.
        # However, we can try to update the Yoast settings if it's Yoast.
        
        print("ℹ️ Note: Direct robots.txt editing via REST API is often blocked by security plugins.")
        print("Suggested fix: Login to WP Admin -> Yoast SEO -> Tools -> File Editor.")
        print("Manual Change Required:")
        print("-" * 30)
        print(new_content)
        print("-" * 30)
    else:
        print("✅ No insecure HTTP links found in robots.txt.")

if __name__ == "__main__":
    main()
