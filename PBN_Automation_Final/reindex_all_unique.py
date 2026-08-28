#!/usr/bin/env python3
"""
Re-index All Unique Posts — Fetches all currently published posts from WordPress 
and submits their URLs to the Google Indexing API. 
This signals Google that the site has been cleaned up and content is ready for crawling.
"""
import requests
import base64
import os
import json
import time
from dotenv import load_dotenv

try:
    from core.indexing_api import submit_to_google_indexing
except ImportError:
    # Try local import if running from PBN_Automation_Final
    sys.path.append('core')
    from indexing_api import submit_to_google_indexing

load_dotenv()

# --- CONFIG ---
SITE_URL = "https://luckybetvip.com"
LOGIN = "admin"
APP_PASSWORD = "4SvP8Q4hqfxnsDo6xS351Xcr"

def get_auth_headers():
    token = base64.b64encode(f"{LOGIN}:{APP_PASSWORD}".encode()).decode()
    return {
        'Authorization': f'Basic {token}',
        'Content-Type': 'application/json'
    }

def fetch_all_published_urls():
    """Fetches all published post and page URLs from WP REST API."""
    urls = []
    headers = get_auth_headers()
    
    for post_type in ['posts', 'pages']:
        page = 1
        print(f"🔍 Fetching {post_type} from {SITE_URL}...")
        
        while True:
            api_url = f"{SITE_URL.rstrip('/')}/wp-json/wp/v2/{post_type}"
            params = {'per_page': 100, 'page': page, 'status': 'publish'}
            try:
                r = requests.get(api_url, headers=headers, params=params, timeout=30)
                if r.status_code != 200:
                    break
                posts = r.json()
                if not posts:
                    break
                for post in posts:
                    link = post.get('link')
                    if link:
                        urls.append(link)
                
                total_pages = int(r.headers.get('X-WP-TotalPages', 1))
                if page >= total_pages:
                    break
                page += 1
            except Exception as e:
                print(f"❌ Error fetching {post_type}: {e}")
                break
    return urls

def main():
    urls = fetch_all_published_urls()
    print(f"📊 Found {len(urls)} unique published URLs.")
    
    if not urls:
        print("⚠️ No URLs found to index.")
        return

    print(f"🚀 Submitting {len(urls)} URLs to Google Indexing API...")
    success_count = 0
    
    for i, url in enumerate(urls):
        print(f"   [{i+1}/{len(urls)}] Submitting: {url}", end=" ")
        try:
            # We use the existing indexing_api logic
            success = submit_to_google_indexing(url)
            if success:
                print("✅")
                success_count += 1
            else:
                print("❌ (API Error)")
        except Exception as e:
            print(f"❌ (Failed: {e})")
        
        # Respect API rate limits (quota is usually 200/day, we have 45)
        time.sleep(1)

    print(f"\n✅ Finished! Successfully submitted {success_count}/{len(urls)} URLs.")
    print("ℹ️ Google will usually crawl these pages within 24-48 hours.")

if __name__ == "__main__":
    main()
