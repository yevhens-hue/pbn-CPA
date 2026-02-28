import requests
import json
import base64
import sys

# Configuration
SITE_URL = "https://luckybetvip.com"
USERNAME = "admin"
APP_PASSWORD = "4SvP8Q4hqfxnsDo6xS351Xcr"

def delete_post_by_slug(slug):
    # Auth
    auth_string = f"{USERNAME}:{APP_PASSWORD}"
    auth_header = base64.b64encode(auth_string.encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/json'
    }
    
    # 1. Get Post ID
    print(f"🔍 Searching for post with slug: {slug}...")
    search_url = f"{SITE_URL}/wp-json/wp/v2/posts?slug={slug}"
    
    try:
        response = requests.get(search_url, headers=headers)
        if response.status_code != 200:
            print(f"❌ Error searching post: {response.text}")
            return
            
        posts = response.json()
        if not posts:
            print("❌ Post not found.")
            return
            
        post_id = posts[0]['id']
        post_title = posts[0]['title']['rendered']
        print(f"✅ Found Post ID: {post_id} ('{post_title}')")
        
        # 2. Delete Post
        print(f"🗑️ Deleting post {post_id}...")
        delete_url = f"{SITE_URL}/wp-json/wp/v2/posts/{post_id}"
        
        # force=true to skip trash and delete permanently
        del_response = requests.delete(delete_url + "?force=true", headers=headers)
        
        if del_response.status_code == 200 or del_response.status_code == 204:
             print(f"✅ Post {post_id} successfully deleted.")
        else:
             print(f"❌ Failed to delete: {del_response.status_code} {del_response.text}")
             
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 delete_post.py <slug>")
        # Default for this task
        target_slug = "random_india_topic-expert-perspective-on-the-issue"
        delete_post_by_slug(target_slug)
    else:
        delete_post_by_slug(sys.argv[1])
