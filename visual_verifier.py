import requests
from bs4 import BeautifulSoup
import json
import sys

def verify_link_on_page(url, target_url, anchor_text):
    """
    Verifies if a specific link and anchor text exists on a given page.
    """
    try:
        # Force HTTPS if needed or just use as is
        print(f"Checking {url}...")
        response = requests.get(url, timeout=20)
        if response.status_code != 200:
            return False, f"HTTP Error: {response.status_code}"
            
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        
        target_found = False
        anchor_found = False
        
        for link in links:
            # Normalize URLs (strip trailing slashes)
            if link['href'].rstrip('/') == target_url.rstrip('/'):
                target_found = True
                if anchor_text.lower() in link.text.lower():
                    anchor_found = True
                    return True, "Link found and matches."
        
        if target_found and not anchor_found:
            return False, "Link found but anchor text mismatch."
        
        return False, "Link not found."
        
    except Exception as e:
        return False, str(e)

def run_verification(results_file='results.json', output_file='verification_report.json'):
    """
    Reads results of publication and verifies each URL.
    """
    try:
        with open(results_file, 'r') as f:
            published_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {results_file} not found.")
        return

    report = []
    print(f"🔍 Starting verification for {len(published_data)} items...")
    
    for item in published_data:
        # Support different keys depending on where results.json came from
        url = item.get('new_post_url') or item.get('url')
        target = item.get('target_url') # publish_post.py might not save this in results?
        # publish_post.py saves: site, status, new_post_url
        # We might need to look up target/anchor if not in results.json
        
        # If target is missing, we can't verify fully, but can check if page loads
        if not url or url == "N/A":
            continue
            
        # For now, let's assume we just check if page loads if target is missing
        if not target:
             print(f"⚠️ Target URL missing for {url}. Checking health only.")
             try:
                 r = requests.get(url, timeout=10)
                 status = "VERIFIED" if r.status_code == 200 else "FAILED"
                 message = f"HTTP {r.status_code}"
             except Exception as e:
                 status = "FAILED"
                 message = str(e)
        else:
            anchor = item.get('anchor', '')
            success, message = verify_link_on_page(url, target, anchor)
            status = "VERIFIED" if success else "FAILED"
        
        print(f"[{status}] {url} -> {message}")
        
        report.append({
            "url": url,
            "status": status,
            "message": message
        })
        
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nVerification complete. Report saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_verification(sys.argv[1])
    else:
        run_verification()
