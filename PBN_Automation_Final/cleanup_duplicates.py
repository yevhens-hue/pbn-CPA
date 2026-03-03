#!/usr/bin/env python3
"""
Cleanup Duplicates — Finds and removes duplicate WordPress posts.
Posts with the same base slug published multiple times (e.g. slug-2, slug-3) 
are identified. The newest version is kept, the rest are trashed.

Usage:
  python3 cleanup_duplicates.py          # Dry run (shows what would be deleted)
  python3 cleanup_duplicates.py --apply  # Actually delete duplicates
"""

import requests
import base64
import re
import sys
import json
import os
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

# --- CONFIG (loaded from data/sites_data.json) ---
def load_site_config():
    paths = ['data/sites_data.json', '../data/sites_data.json', 'PBN_Automation_Final/data/sites_data.json']
    for p in paths:
        if os.path.exists(p):
            with open(p) as f:
                sites = json.load(f)
                if sites:
                    return sites[0]
    # Fallback hardcoded
    return {
        "site_url": "https://luckybetvip.com",
        "login": "admin",
        "app_password": "4SvP8Q4hqfxnsDo6xS351Xcr"
    }

def get_auth_headers(login, app_password):
    token = base64.b64encode(f"{login}:{app_password}".encode()).decode()
    return {
        'Authorization': f'Basic {token}',
        'Content-Type': 'application/json'
    }

def normalize_slug(slug):
    """
    Strips trailing -N suffix to find the base slug.
    e.g. 'aviator-game-tricks-2026-3' → 'aviator-game-tricks-2026'
    """
    return re.sub(r'-(\d+)$', '', slug)

def fetch_all_posts(site_url, headers):
    """Fetches ALL published posts via WP REST API (paginated)."""
    all_posts = []
    page = 1
    while True:
        url = f"{site_url.rstrip('/')}/wp-json/wp/v2/posts"
        params = {'per_page': 100, 'page': page, 'status': 'publish'}
        try:
            r = requests.get(url, headers=headers, params=params, timeout=30)
            if r.status_code != 200:
                break
            posts = r.json()
            if not posts:
                break
            all_posts.extend(posts)
            # Check if there are more pages
            total_pages = int(r.headers.get('X-WP-TotalPages', 1))
            if page >= total_pages:
                break
            page += 1
        except Exception as e:
            print(f"❌ Error fetching page {page}: {e}")
            break
    return all_posts

def find_duplicates(posts):
    """
    Groups posts by their normalized slug. 
    Returns dict of { base_slug: [list of posts with that base slug] }
    Only includes groups with 2+ posts (actual duplicates).
    """
    groups = defaultdict(list)
    for post in posts:
        slug = post.get('slug', '')
        base = normalize_slug(slug)
        groups[base].append(post)
    
    # Filter to only duplicate groups
    return {k: v for k, v in groups.items() if len(v) > 1}

def delete_post(site_url, headers, post_id, force=False):
    """Deletes (trashes) a WordPress post."""
    url = f"{site_url.rstrip('/')}/wp-json/wp/v2/posts/{post_id}"
    params = {'force': force}  # force=True permanently deletes
    try:
        r = requests.delete(url, headers=headers, params=params, timeout=15)
        return r.status_code == 200
    except Exception as e:
        print(f"   ❌ Error deleting post {post_id}: {e}")
        return False

def main():
    dry_run = "--apply" not in sys.argv
    
    config = load_site_config()
    site_url = config['site_url']
    headers = get_auth_headers(config['login'], config['app_password'])
    
    print(f"🔍 Scanning {site_url} for duplicate posts...")
    if dry_run:
        print("   ℹ️  DRY RUN mode. Use --apply to actually delete.\n")
    
    posts = fetch_all_posts(site_url, headers)
    print(f"📊 Total published posts: {len(posts)}\n")
    
    duplicates = find_duplicates(posts)
    
    if not duplicates:
        print("✅ No duplicates found! Your site is clean.")
        return
    
    total_to_delete = 0
    posts_to_delete = []
    
    for base_slug, group in sorted(duplicates.items()):
        # Sort by date descending — keep the newest
        group.sort(key=lambda p: p.get('date', ''), reverse=True)
        keeper = group[0]
        to_remove = group[1:]
        
        print(f"📌 Base: {base_slug}")
        print(f"   ✅ KEEP: [{keeper['id']}] {keeper['slug']} ({keeper['date'][:10]})")
        for dup in to_remove:
            print(f"   🗑️  DELETE: [{dup['id']}] {dup['slug']} ({dup['date'][:10]})")
            posts_to_delete.append(dup)
            total_to_delete += 1
        print()
    
    print(f"{'='*60}")
    print(f"📊 Summary: {len(duplicates)} duplicate groups, {total_to_delete} posts to delete")
    print(f"{'='*60}\n")
    
    if dry_run:
        print("🔒 DRY RUN — no posts were deleted.")
        print("   Run with --apply to execute deletion.")
        return
    
    # Apply deletion
    deleted = 0
    for post in posts_to_delete:
        print(f"🗑️  Deleting [{post['id']}] {post['slug']}...", end=" ")
        if delete_post(site_url, headers, post['id']):
            print("✅")
            deleted += 1
        else:
            print("❌ FAILED")
    
    print(f"\n✅ Done! Deleted {deleted}/{total_to_delete} duplicate posts.")
    print(f"   Remaining unique posts: {len(posts) - deleted}")

if __name__ == "__main__":
    main()
