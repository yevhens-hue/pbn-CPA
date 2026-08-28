import requests
import json
import base64
import os

def update_app_page():
    from dotenv import load_dotenv
    load_dotenv()
    
    site_url = os.getenv("SITE_URL", "https://luckybetvip.com")
    login = os.getenv("WP_USER", "admin")
    password = os.getenv("WP_APP_PWD", "")
    page_id = int(os.getenv("APP_PAGE_ID", "12"))
    target_link = os.getenv(
        "TARGET_LINK",
        "https://refpa14435.com/L?tag=d_5300195m_1236c_&site=5300195&ad=1236&url=ru%2Fgames%2Fcrash"
    )
    
    auth_string = f"{login}:{password}"
    auth_header = base64.b64encode(auth_string.encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/json'
    }
    
    html_content = f"""
<style>
/* 1. Hide Sidebar & Make Full Width */
#right-sidebar {{ display: none !important; }}
#primary {{ width: 100% !important; float: none !important; margin: 0 !important; max-width: 100% !important; }}
.site-content .content-area {{ max-width: 100% !important; }}

/* 2. Glassmorphism Styles */
.app-landing {{
    font-family: 'Inter', sans-serif;
    color: #e2e8f0;
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 20px;
}}
.glass-card {{
    background: rgba(30, 41, 59, 0.7);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}
.hero-section {{
    text-align: center;
    margin-bottom: 40px;
}}
.hero-badge {{
    background: #e11d48;
    color: white;
    padding: 4px 12px;
    border-radius: 99px;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    display: inline-block;
    margin-bottom: 15px;
}}
.download-btn {{
    display: inline-block;
    background: linear-gradient(135deg, #facc15, #eab308);
    color: #000 !important;
    padding: 18px 45px;
    border-radius: 12px;
    font-size: 1.25rem;
    font-weight: 800;
    text-decoration: none !important;
    transition: all 0.3s ease;
    box-shadow: 0 10px 20px rgba(234, 179, 8, 0.3);
    margin-top: 25px;
}}
.download-btn:hover {{
    transform: translateY(-3px);
    box-shadow: 0 15px 30px rgba(234, 179, 8, 0.4);
}}
.spec-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 30px 0;
    background: rgba(15, 23, 42, 0.5);
    border-radius: 10px;
    overflow: hidden;
}}
.spec-table td, .spec-table th {{
    padding: 15px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    text-align: left;
}}
.install-step {{
    display: flex;
    gap: 15px;
    margin-bottom: 20px;
    align-items: flex-start;
}}
.step-num {{
    background: #e11d48;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    flex-shrink: 0;
}}
</style>

<div class="app-landing">
    <div class="glass-card">
        <div class="hero-section">
            <span class="hero-badge">Verified 2026 APK</span>
            <h1 style="color: #fff; font-size: 2.5rem; margin-bottom: 10px;">Download Aviator App</h1>
            <p style="font-size: 1.1rem; color: #94a3b8;">Experience the #1 Crash Game in India with Instant Withdrawals and 24/7 Support.</p>
            <a href="{target_link}" class="download-btn">🚀 DOWNLOAD APK NOW</a>
            <p style="font-size: 0.8rem; color: #64748b; margin-top: 15px;">Size: 18.4 MB | Version: 4.8.2 | Supports Android & iOS</p>
        </div>

        <h2 style="color: #facc15; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px;">📊 Technical Specifications</h2>
        <table class="spec-table">
            <tr><th>OS Compatibility</th><td>Android 5.0+, iOS 11.0+</td></tr>
            <tr><th>Latest Update</th><td>March 2026</td></tr>
            <tr><th>Promo Code</th><td><strong>1x_4393603</strong> (130% Bonus)</td></tr>
            <tr><th>License</th><td>Curacao eGaming (Official)</td></tr>
        </table>

        <h2 style="color: #facc15; margin-top: 40px;">📲 How to Install Aviator APK</h2>
        <div class="install-steps">
            <div class="install-step">
                <div class="step-num">1</div>
                <div><strong>Download the File:</strong> Click the button above to start downloading the Aviator APK file.</div>
            </div>
            <div class="install-step">
                <div class="step-num">2</div>
                <div><strong>Allow Unknown Sources:</strong> Go to Settings > Security and enable "Install from Unknown Sources".</div>
            </div>
            <div class="install-step">
                <div class="step-num">3</div>
                <div><strong>Install & Login:</strong> Open the downloaded file, click install, and log in with your account. Don't forget to use the promo code for the bonus!</div>
            </div>
        </div>
        
        <div style="background: rgba(225, 29, 72, 0.1); border-left: 4px solid #e11d48; padding: 20px; border-radius: 8px; margin-top: 30px;">
            <p style="margin: 0;"><strong>⚠️ Notice:</strong> Always download the app from our verified links to ensure you have the latest secure version with official multipliers.</p>
        </div>
    </div>
</div>
    """
    
    payload = {
        'content': html_content,
        'title': "Download Aviator App (Official APK)"
    }
    
    endpoint = f"{site_url}/wp-json/wp/v2/pages/{page_id}"
    
    print(f"📡 Updating page {page_id} on {site_url}...")
    try:
        resp = requests.post(endpoint, headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            print(f"✅ Page updated successfully! URL: {resp.json().get('link')}")
        else:
            print(f"❌ Failed to update page. Status: {resp.status_code}, Response: {resp.text}")
    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    update_app_page()
