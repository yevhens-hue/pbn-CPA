import os
import requests
import random
import time
import base64
from dotenv import load_dotenv
import threading

# Add parent dir to path so we can import publish_post
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from publish_post import send_telegram_post
except ImportError:
    print("❌ Could not import send_telegram_post from publish_post.py")
    sys.exit(1)

# Load environment variables
load_dotenv()

def get_random_published_posts(site_url, username, app_password, count=3):
    """
    Fetches random published posts from WordPress REST API.
    """
    auth_string = f"{username}:{app_password}"
    auth_header = base64.b64encode(auth_string.encode()).decode()
    headers = {'Authorization': f'Basic {auth_header}'}
    
    endpoint = f"{site_url.rstrip('/')}/wp-json/wp/v2/posts"
    # Get the latest 50 posts to pick from
    params = {'status': 'publish', 'per_page': 50, 'orderby': 'date', 'order': 'desc'}
    
    try:
        response = requests.get(endpoint, headers=headers, params=params, timeout=30)
        if response.status_code == 200:
            posts = response.json()
            if posts:
                # Select random posts
                selected = random.sample(posts, min(count, len(posts)))
                return selected
        else:
            print(f"❌ Error fetching from WP API: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Error finding posts: {e}")
        
    return []

def run_backfill(count=3):
    """
    Main orchestrator for Telegram backfilling.
    """
    import json
    target_site = None
    
    try:
        with open('data/sites_data.json', 'r') as f:
            sites = json.load(f)
            for site in sites:
                url = site.get('site_url', '')
                if "luckybetvip.com" in url or "games-income.com" in url:
                    target_site = site
                    break
    except Exception as e:
        print(f"⚠️ Error reading sites_data.json: {e}")
            
    if not target_site:
        print("❌ Could not find a valid site in sites_data.json. Exiting.")
        return
        
    site_url = target_site.get('site_url')
    username = target_site.get('login')
    app_password = target_site.get('app_password')
    
    print(f"🚀 Starting Telegram Social Signal Backfill for {site_url}...")
    posts = get_random_published_posts(site_url, username, app_password, count=count)
    
    if not posts:
        print("⚠️ No posts found to backfill.")
        return
        
    for i, post in enumerate(posts):
        title = post.get('title', {}).get('rendered', 'Unknown Title')
        # Clean up HTML entities in title
        import html
        title = html.unescape(title)
        
        link = post.get('link', '')
        
        print(f"[{i+1}/{len(posts)}] Sending {title} to Telegram...")
        send_telegram_post(title, link, title)
        
        if i < len(posts) - 1:
            delay = random.randint(15, 45)
            print(f"⏱ Waiting {delay}s before next post...")
            time.sleep(delay)
            
    print("✅ Backfill complete.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Backfill old WP posts to Telegram.")
    parser.add_argument("--count", type=int, default=3, help="Number of random posts to send.")
    args = parser.parse_args()
    
    run_backfill(count=args.count)
