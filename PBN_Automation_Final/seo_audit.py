#!/usr/bin/env python3
"""
SEO Audit Script — PageSpeed Insights + Core Web Vitals
Checks performance scores for published site URLs.

Usage:
  python3 seo_audit.py
  python3 seo_audit.py https://luckybetvip.com/your-post/
"""

import sys
import json
import requests
import os
import re
from datetime import datetime

# --- CONFIG ---
PSI_API_KEY = os.getenv("GOOGLE_PSI_API_KEY", "")  # Optional. Without key: 2 req/sec limit.
DEFAULT_URLS = [
    "https://luckybetvip.com/",
    "https://luckybetvip.com/aviator-game-hints-tricks-2026-insider-secrets-2026-strategy-guide/"
]

PSI_ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

def check_pagespeed(url, strategy="mobile"):
    """
    Calls PageSpeed Insights API for a given URL.
    Returns dict with key metrics or None on error.
    """
    params = {
        "url": url,
        "strategy": strategy,  # 'mobile' or 'desktop'
        "category": "performance",
    }
    if PSI_API_KEY:
        params["key"] = PSI_API_KEY

    try:
        print(f"  📡 Checking {strategy}: {url}")
        response = requests.get(PSI_ENDPOINT, params=params, timeout=30)
        if response.status_code != 200:
            print(f"  ❌ API Error {response.status_code}")
            return None

        data = response.json()
        lhr = data.get("lighthouseResult", {})
        categories = lhr.get("categories", {})
        audits = lhr.get("audits", {})

        score = int(categories.get("performance", {}).get("score", 0) * 100)

        # Core Web Vitals
        lcp = audits.get("largest-contentful-paint", {}).get("displayValue", "N/A")
        cls = audits.get("cumulative-layout-shift", {}).get("displayValue", "N/A")
        fid = audits.get("max-potential-fid", {}).get("displayValue", "N/A")
        ttfb = audits.get("server-response-time", {}).get("displayValue", "N/A")
        tbt = audits.get("total-blocking-time", {}).get("displayValue", "N/A")

        return {
            "url": url,
            "strategy": strategy,
            "performance_score": score,
            "LCP": lcp,
            "CLS": cls,
            "FID_potential": fid,
            "TTFB": ttfb,
            "TBT": tbt,
        }

    except Exception as e:
        print(f"  ❌ Request failed: {e}")
        return None


def grade_score(score):
    if score >= 90: return "🟢 GOOD"
    if score >= 50: return "🟡 NEEDS IMPROVEMENT"
    return "🔴 POOR"

def check_broken_links(url):
    """Fetches the page and checks all <a> tags for 200 OK status."""
    print(f"  🔗 Checking for broken links on: {url}")
    broken = []
    try:
        r = requests.get(url, timeout=20)
        if r.status_code != 200:
            return [f"Page itself returned {r.status_code}"]
        
        # Simple Regex to find all hrefs in <a> tags
        links = re.findall(r'href=["\'](http[s]?://.*?)["\']', r.text)
        for link in set(links):
             try:
                 lr = requests.head(link, timeout=10, allow_redirects=True)
                 if lr.status_code >= 400:
                     broken.append(f"{link} (Status: {lr.status_code})")
             except:
                 broken.append(f"{link} (Connection Failed)")
        
        return broken
    except Exception as e:
        return [f"Crawler failed: {e}"]

def check_keyword_cannibalization(urls):
    """Checks if multiple URLs are targeting the same primary keywords."""
    print("\n🔍 Checking for Keyword Cannibalization...")
    keywords = {}
    issues = []
    
    # Common stop words to ignore in simple analysis
    stop_words = {'the', 'how', 'to', 'for', 'and', 'in', 'on', 'top', 'best', '2026', 'review', 'guide'}
    
    for url in urls:
        # Extract keywords from URL slug
        slug = url.rstrip('/').split('/')[-1]
        words = [w for w in re.split(r'[-_]', slug.lower()) if len(w) > 3 and w not in stop_words]
        
        # Key is sorted tuple of words (rudimentary)
        key = " ".join(sorted(words[:2])) 
        if key in keywords:
            keywords[key].append(url)
        else:
            keywords[key] = [url]
            
    for key, sites in keywords.items():
        if len(sites) > 1:
            issues.append(f"⚠️ Conflict on keyword '{key}': {', '.join(sites)}")
            
    return issues

def check_serp_with_playwright(keyword, target_domain="luckybetvip.com"):
    """
    (Playwright Feature 2: Smart SEO Audit)
    Scrapes Google Search using Playwright to bypass easy blocks and find our ranking.
    """
    print(f"\n🔍 Playwright: Checking Google for '{keyword}'...")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            # Navigate to google and search
            page.goto(f"https://www.google.com/search?q={keyword}&hl=en", timeout=30000)
            
            # Simple check for domain in results text
            results = page.locator("div.g").all_inner_texts()
            browser.close()
            
            for index, res in enumerate(results):
                if target_domain in res:
                     return f"✅ '{keyword}': Ranked #{index + 1} on Page 1"
            
            return f"❌ '{keyword}': Not found on Page 1"
            
    except Exception as e:
         return f"⚠️ Playwright SERP failed: {e}"


def print_report(result):
    if not result:
        return
    print(f"\n  📊 Performance Score: {result['performance_score']} — {grade_score(result['performance_score'])}")
    print(f"  ⏱️  LCP  : {result['LCP']}")
    print(f"  📐 CLS  : {result['CLS']}")
    print(f"  ⚡ TBT  : {result['TBT']}")
    print(f"  🌐 TTFB : {result['TTFB']}")


def run_audit(urls):
    all_results = []
    print(f"\n🔍 SEO Audit — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    for url in urls:
        print(f"\n🌐 URL: {url}")
        mobile = check_pagespeed(url, strategy="mobile")
        desktop = check_pagespeed(url, strategy="desktop")
        broken_links = check_broken_links(url)

        print("\n  [📱 Mobile]")
        print_report(mobile)
        print("\n  [🖥️  Desktop]")
        print_report(desktop)

        if broken_links:
            print(f"\n  ⚠️  Broken Links Found: {len(broken_links)}")
            for bl in broken_links:
                print(f"     - {bl}")
        else:
             print("\n  ✅ No broken links found.")

        if mobile: 
            mobile['broken_links'] = broken_links
            all_results.append(mobile)
        if desktop: all_results.append(desktop)

    # Cannibalization check
    cannibal_issues = check_keyword_cannibalization(urls)
    if cannibal_issues:
        for issue in cannibal_issues:
            print(issue)

    # Save report
    report_path = "seo_audit_report.json"
    with open(report_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\n✅ Audit complete. Report saved to: {report_path}")


if __name__ == "__main__":
    urls = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_URLS
    run_audit(urls)
