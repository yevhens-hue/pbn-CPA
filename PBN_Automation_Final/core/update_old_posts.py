import requests
import json
import base64
import os
import datetime
import time
from dotenv import load_dotenv

load_dotenv()

def get_old_wp_posts(site_url, username, app_password, before_date=None):
    """Fetches posts published before a certain date."""
    auth_string = f"{username}:{app_password}"
    auth_header = base64.b64encode(auth_string.encode()).decode()
    headers = {'Authorization': f'Basic {auth_header}'}
    
    endpoint = f"{site_url.rstrip('/')}/wp-json/wp/v2/posts"
    params = {
        'status': 'publish',
        'per_page': 20,
        'orderby': 'date',
        'order': 'asc' # Oldest first
    }
    if before_date:
        params['before'] = before_date
        
    try:
        resp = requests.get(endpoint, headers=headers, params=params, timeout=30)
        if resp.status_code == 200:
            return resp.json()
        return []
    except Exception as e:
        print(f"⚠️ Error fetching old posts: {e}")
        return []

def refresh_content_ai(title, old_content):
    """Uses Gemini to refresh old content for 2026."""
    gemini_key = os.getenv('GEMINI_API_KEY', '').strip()
    if not gemini_key:
        return old_content
        
    prompt = f"""
    You are a professional SEO editor. Your task is to refresh an old iGaming article for the year 2026.
    
    Current Title: {title}
    
    Requirements:
    1. **Update Year**: Change any mentions of 2023, 2024, or 2025 to "**2026**".
    2. **Add Value**: Add a new 200-word section titled "2026 Insider Strategy Update" with specific, actionable tips.
    3. **Expertise**: Use E-E-A-T signals (e.g., "In my latest testing in January 2026...").
    4. **Maintain Style**: Keep the existing promotion links and structure.
    5. **Return Valid HTML**: Do not include markdown or wrapping tags.
    
    Original Content:
    {old_content}
    """
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        if resp.status_code == 200:
            result = resp.json()
            new_content = result['candidates'][0]['content']['parts'][0]['text']
            return new_content.replace('```html', '').replace('```', '')
    except Exception as e:
        print(f"⚠️ AI Refresh failed: {e}")
    return old_content

def update_wp_post(site_url, username, app_password, post_id, new_content):
    """Updates an existing post on WordPress."""
    auth_string = f"{username}:{app_password}"
    auth_header = base64.b64encode(auth_string.encode()).decode()
    headers = {'Authorization': f'Basic {auth_header}'}
    
    endpoint = f"{site_url.rstrip('/')}/wp-json/wp/v2/posts/{post_id}"
    
    # We purposefully don't change the status, just the content and potentially the date
    payload = {
        'content': new_content,
        'date': datetime.datetime.now().isoformat() # This forces it as "freshly updated"
    }
    
    try:
        resp = requests.post(endpoint, headers=headers, json=payload, timeout=30)
        return resp.status_code == 200
    except Exception as e:
        print(f"⚠️ Error updating post {post_id}: {e}")
        return False

def run_freshness_cycle():
    # In a real scenario, we'd loop through sites_data.json
    # For now, let's target the main site
    site_url = "https://luckybetvip.com"
    user = os.getenv("WP_USER")
    pwd = os.getenv("WP_APP_PWD")
    
    if not all([site_url, user, pwd]):
        print("❌ Credentials missing.")
        return

    print(f"♻️ Starting Content Freshness Cycle for {site_url}...")
    # Fetch posts older than 1 month
    one_month_ago = (datetime.datetime.now() - datetime.timedelta(days=30)).isoformat()
    old_posts = get_old_wp_posts(site_url, user, pwd, before_date=one_month_ago)
    
    if not old_posts:
        print("✅ All posts are fresh!")
        return

    print(f"📋 Found {len(old_posts)} old posts to refresh.")
    
    for post in old_posts[:2]: # Limit to 2 per run to avoid mass-spam detection
        post_id = post['id']
        title = post['title']['rendered']
        content = post['content']['rendered']
        
        print(f"   🔄 Refreshing: {title} (ID: {post_id})...")
        refreshed_html = refresh_content_ai(title, content)
        
        if refreshed_html != content:
            if update_wp_post(site_url, user, pwd, post_id, refreshed_html):
                print(f"   ✨ Successfully updated: {title}")
            else:
                print(f"   ❌ Failed to update: {title}")
        else:
            print(f"   ℹ️ No changes needed for: {title}")
            
if __name__ == "__main__":
    run_freshness_cycle()
