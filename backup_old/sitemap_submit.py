#!/usr/bin/env python3
"""
Sitemap Submitter + Validator
Checks that your sitemap is valid and notifies Google/Bing of updates.

Usage:
  python3 sitemap_submit.py                      # Check default site
  python3 sitemap_submit.py https://mysite.com   # Check specific site
"""

import sys
import requests
import xml.etree.ElementTree as ET
from datetime import datetime


SITEMAP_PATHS = [
    '/sitemap_index.xml',   # Yoast SEO
    '/sitemap.xml',         # Standard
    '/post-sitemap.xml',    # Yoast Posts
]

DEFAULT_SITE = "https://luckybetvip.com"


def find_sitemap(site_url):
    """Try common sitemap paths and return the first working one."""
    for path in SITEMAP_PATHS:
        url = site_url.rstrip('/') + path
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200 and ('xml' in r.headers.get('Content-Type', '') or '<urlset' in r.text or '<sitemapindex' in r.text):
                return url
        except Exception:
            pass
    return None


def count_sitemap_urls(sitemap_url):
    """Parse sitemap and count total URLs."""
    try:
        r = requests.get(sitemap_url, timeout=15)
        root = ET.fromstring(r.text)
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        # Sitemap Index — has nested sitemaps
        sitemaps = root.findall('sm:sitemap', ns)
        if sitemaps:
            total = 0
            for sm in sitemaps:
                loc = sm.find('sm:loc', ns)
                if loc is not None:
                    sub_count = count_sitemap_urls(loc.text)
                    total += sub_count
            return total
        
        # Regular sitemap — has URLs directly
        urls = root.findall('sm:url', ns)
        return len(urls)
        
    except Exception as e:
        print(f"  ⚠️ Error parsing sitemap: {e}")
        return 0


def submit_to_google(sitemap_url):
    """
    Pings Google to notify about sitemap update.
    Note: Google Ping API was deprecated in 2023. 
    The correct method is Google Search Console API (requires OAuth).
    This function does the old ping for reference.
    """
    ping_url = f"https://www.google.com/ping?sitemap={sitemap_url}"
    try:
        r = requests.get(ping_url, timeout=10)
        if r.status_code == 200:
            print(f"  ✅ Google pinged: {ping_url}")
        else:
            print(f"  ⚠️ Google ping returned {r.status_code}. Use Google Search Console instead.")
    except Exception as e:
        print(f"  ❌ Google ping failed: {e}")


def submit_to_bing(sitemap_url):
    """Pings Bing IndexNow (still works!)."""
    ping_url = f"https://www.bing.com/ping?sitemap={sitemap_url}"
    try:
        r = requests.get(ping_url, timeout=10)
        if r.status_code == 200:
            print(f"  ✅ Bing pinged!")
        else:
            print(f"  ⚠️ Bing ping returned {r.status_code}")
    except Exception as e:
        print(f"  ❌ Bing ping failed: {e}")


def check_robots_txt(site_url):
    """Check robots.txt is allowing Google and pointing to sitemap."""
    url = site_url.rstrip('/') + '/robots.txt'
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            content = r.text
            print(f"\n  📄 robots.txt found ({len(content)} chars)")
            if 'Disallow: /' in content and not 'Allow: /' in content:
                print("  🔴 WARNING: robots.txt may be blocking all crawlers!")
            else:
                print("  ✅ robots.txt looks fine")
            if 'Sitemap:' in content:
                print("  ✅ robots.txt includes Sitemap reference")
            else:
                print("  ⚠️ robots.txt doesn't mention sitemap — add: Sitemap: " + site_url + "/sitemap_index.xml")
        else:
            print(f"  ⚠️ robots.txt not found ({r.status_code})")
    except Exception as e:
        print(f"  ❌ robots.txt check failed: {e}")


def run(site_url):
    print(f"\n🗺️ Sitemap Check — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"🌐 Site: {site_url}")
    print("=" * 60)

    # Find sitemap
    sitemap_url = find_sitemap(site_url)
    if not sitemap_url:
        print("❌ No sitemap found! Install Yoast SEO or create sitemap.xml manually.")
        return

    print(f"\n✅ Sitemap found: {sitemap_url}")
    
    # Count URLs
    count = count_sitemap_urls(sitemap_url)
    print(f"📊 Total URLs in sitemap: {count}")
    if count < 5:
        print("⚠️ Very few URLs indexed — check your site content and permalink settings.")

    # Robots.txt
    check_robots_txt(site_url)

    # Submit
    print(f"\n📡 Submitting sitemap to search engines...")
    submit_to_google(sitemap_url)
    submit_to_bing(sitemap_url)

    print("\n✅ Done! Also manually submit to Google Search Console:")
    print(f"   https://search.google.com/search-console → Sitemaps → {sitemap_url}")


if __name__ == '__main__':
    site = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SITE
    run(site)
