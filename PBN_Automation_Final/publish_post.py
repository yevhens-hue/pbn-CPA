import requests
import json
import base64
import sys
import os
import warnings
import datetime
import random
import time
from dotenv import load_dotenv

# Google Sheets & SEO Imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from core.indexing_api import submit_to_google_indexing
from core.seo_optimizer import generate_game_schema, generate_faq_schema, generate_review_schema, get_updated_title, generate_whatsapp_cta, get_random_indian_city

# Suppress noisy warnings
warnings.filterwarnings("ignore", category=FutureWarning)
try:
    from urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
except:
    pass

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
SHEET_ID = "1CJjN_mSwrGwp2tVuaLK0vENb2c5VnYPQw0JM43HTE-c" # ID вашей таблицы
SHEET_TAB_NAME = "Report" # Имя вкладки для отчетов

# Unified 11-column structure mapping
SHEET_HEADERS = ['Time', 'Site URL', 'Login', 'App Password', 'Target Link', 'Anchor Text', 'Article Topic', 'Author Style', 'Status', 'Post URL', 'Model Used']

# Stock Images for Injection (Aviator/Gambling/India Theme)
GAMBLING_IMAGES = [
    # WebP format — 30-40% smaller than JPEG/PNG → faster Core Web Vitals
    "https://images.unsplash.com/photo-1605870445919-838d190e8e1e?auto=format&fit=crop&w=1200&q=80&fm=webp",  # Poker Chips
    "https://images.unsplash.com/photo-1596838132731-3301c3fd4317?auto=format&fit=crop&w=1200&q=80&fm=webp",  # Casino Lights
    "https://images.unsplash.com/photo-1518133910546-b6c2fb7d79e3?auto=format&fit=crop&w=1200&q=80&fm=webp",  # Playing Cards
    "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=1200&q=80&fm=webp",  # Gaming Setup
    "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?auto=format&fit=crop&w=1200&q=80&fm=webp",  # Money/Currency
    "https://images.unsplash.com/photo-1563941406054-949f42e9d1e5?auto=format&fit=crop&w=1200&q=80&fm=webp",  # Aviator/Plane
    "https://images.unsplash.com/photo-1626277053529-a9b53f7ce03b?auto=format&fit=crop&w=1200&q=80&fm=webp",  # Casino Table India
    "https://images.unsplash.com/photo-1677442135703-1787eea5ce01?auto=format&fit=crop&w=1200&q=80&fm=webp",  # Mobile Gambling
]

# Prompts are now strictly English + Indian Context
STYLE_PROMPTS = {
    "expert": "Write in a dry, analytical, and technical style. Use professional terminology, data, and deep analysis. Minimal emotion, maximum facts.",
    "lifestyle": "Write in an emotional, easy-going, and accessible style. Use personal examples, storytelling, and address the reader as 'you'. It should feel like a personal blog post.",
    "neutral": "Write in a standard informational style typical of a news portal. Objective and balanced."
}

def generate_ai_image(topic):
    """Generates a unique image using OpenAI DALL-E 3."""
    client_key = os.getenv("OPENAI_API_KEY")
    if not client_key:
        return None
    
    print(f"🎨 Generating AI image for topic: {topic}...")
    try:
        # We target a specific prompt style for gambling/India
        prompt = f"Professional high-quality photography, {topic}, Indian context, luxury casino aesthetic, bokeh background, 4k resolution, no text."
        resp = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers={"Authorization": f"Bearer {client_key}"},
            json={
                "model": "dall-e-3",
                "prompt": prompt,
                "n": 1,
                "size": "1024x1024"
            },
            timeout=60
        )
        if resp.status_code == 200:
            url = resp.json()['data'][0]['url']
            print(f"   ✅ AI Image generated: {url[:60]}...")
            return url
    except Exception as e:
        print(f"   ⚠️ AI Image generation failed: {e}")
    return None

# --- HELPER FUNCTIONS ---

def load_content_plan(file_path="data/content_plan_india.json"):
    try:
        # Check if file exists locally or in parent dir
        if not os.path.exists(file_path):
            # Fallback for different CWD
            if os.path.exists(f"../{file_path}"):
                file_path = f"../{file_path}"
            elif os.path.exists(f"PBN_Automation_Final/{file_path}"):
                file_path = f"PBN_Automation_Final/{file_path}"
        
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data.get("topics", [])
    except Exception as e:
        print(f"⚠️ Error loading content plan: {e}")
        return []

# --- SEO & E-E-A-T HELPERS ---

def trigger_onesignal_notification(title, url):
    """
    Triggers a Web Push notification via OneSignal API.
    """
    app_id = os.getenv("ONESIGNAL_APP_ID")
    api_key = os.getenv("ONESIGNAL_REST_API_KEY")
    
    if not app_id or not api_key:
        # Silently skip if not configured
        return False
        
    print(f"   🔔 Triggering OneSignal Push Notification...")
    header = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Basic {api_key}"
    }
    payload = {
        "app_id": app_id,
        "included_segments": ["All"],
        "contents": {"en": f"New Winning Strategy: {title}"},
        "headings": {"en": "🚀 New Aviator Signal!"},
        "url": url
    }
    
    try:
        response = requests.post(
            "https://onesignal.com/api/v1/notifications",
            headers=header,
            json=payload,
            timeout=10
        )
        if response.status_code == 200:
            print("   ✅ Notification sent successfully!")
            return True
        else:
            print(f"   ⚠️ OneSignal Error: {response.text}")
            return False
    except Exception as e:
        print(f"   ⚠️ OneSignal Trigger Failed: {e}")
        return False


def generate_dynamic_aviator_table():
    """Generates a realistic-looking HTML table with 'recent' game data."""
    rounds = []
    for i in range(1, 11):
        multiplier = round(random.uniform(1.01, 15.5), 2)
        status = "Crash" if multiplier < 1.5 else "Win"
        rounds.append(f"<tr><td>#{random.randint(450000, 460000)}</td><td>{multiplier}x</td><td>{status}</td></tr>")
    
    table_html = f"""
    <div class="dynamic-data-table" style="margin: 25px 0; border: 1px solid #ddd; border-radius: 8px; overflow: hidden;">
        <h3 style="background: #f4f4f4; margin: 0; padding: 10px; font-size: 16px;">Live Statistics: Recent Aviator Rounds (India Server)</h3>
        <table style="width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 14px;">
            <thead style="background: #2c3e50; color: #fff;">
                <tr><th style="padding: 10px; text-align: left;">Round ID</th><th style="padding: 10px; text-align: left;">Multiplier</th><th style="padding: 10px; text-align: left;">Signal Status</th></tr>
            </thead>
            <tbody>
                {" ".join(rounds)}
            </tbody>
        </table>
        <p style="padding: 10px; margin: 0; font-size: 12px; color: #666;">*Data updated in real-time based on local server latency.</p>
    </div>
    """
    return table_html

def generate_calculator_html():
    """Returns a JS-based interactive profit calculator to increase time-on-page."""
    calc_html = """
    <div id="aviator-calc" style="background: #111; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 25px; margin: 30px 0; font-family: 'Inter', sans-serif; color: #ededed !important;">
        <h3 style="margin-top: 0; color: #ffffff !important;">🧮 Aviator Profit Calculator</h3>
        <p style="font-size: 14px; color: #a1a1a1 !important;">Estimate your potential winnings based on your bet and target multiplier.</p>
        <div style="margin-bottom: 15px;">
            <label style="display: block; margin-bottom: 5px; font-weight: bold; color: #ededed !important;">Bet Amount (INR):</label>
            <input type="number" id="calc_bet" value="500" style="width: 100%; padding: 12px; background: #000; border: 1px solid #333; border-radius: 8px; color: #fff; font-size: 16px;">
        </div>
        <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 5px; font-weight: bold; color: #ededed !important;">Target Multiplier (x):</label>
            <input type="number" id="calc_mult" value="2.0" step="0.1" style="width: 100%; padding: 12px; background: #000; border: 1px solid #333; border-radius: 8px; color: #fff; font-size: 16px;">
        </div>
        <button onclick="calculateProfit()" style="background: #ffffff; color: #000000; border: none; padding: 14px 20px; border-radius: 8px; cursor: pointer; width: 100%; font-weight: 700; font-size: 16px; transition: transform 0.2s;">Calculate Winnings</button>
        <div id="calc_result" style="margin-top: 20px; padding: 20px; background: #000; border-radius: 8px; display: none; text-align: center; border: 1px solid #ff0040;">
            <span style="font-size: 14px; color: #a1a1a1;">Potential Payout:</span><br>
            <strong style="font-size: 28px; color: #ffffff;" id="final_profit">₹0</strong>
        </div>
        <script>
            function calculateProfit() {
                var bet = document.getElementById('calc_bet').value;
                var mult = document.getElementById('calc_mult').value;
                var result = bet * mult;
                document.getElementById('final_profit').innerText = '₹' + Math.round(result).toLocaleString('en-IN');
                document.getElementById('calc_result').style.display = 'block';
                if (typeof gtag === 'function') {
                    gtag('event', 'calculator_use', {
                        'event_category': 'engagement',
                        'event_label': 'Aviator Profit Calculator'
                    });
                }
            }
        </script>
    </div>
    """
    return calc_html

def get_used_topics(results_file="results.json"):
    """
    Parses results.json to find topics that have already been successfully published.
    """
    try:
        if not os.path.exists(results_file):
            if os.path.exists(f"../{results_file}"):
                results_file = f"../{results_file}"
            elif os.path.exists(f"PBN_Automation_Final/{results_file}"):
                 results_file = f"PBN_Automation_Final/{results_file}"
        
        if not os.path.exists(results_file):
            return set()

        with open(results_file, 'r') as f:
            data = json.load(f)
            # Assuming 'topic' or 'article_topic' is stored. If not, we might need to parse URL or title.
            # Ideally, results.json should store the topic used.
            used = set()
            for item in data:
                if item.get('status') == 'success':
                    # Extract topic from somewhere. Currently results.json stores 'topic' in some versions?
                    # Let's assume we start storing 'topic' in results in this update.
                    if 'topic' in item:
                        used.add(item['topic'])
            return used
    except Exception as e:
        print(f"⚠️ Error reading results.json: {e}")
        return set()

def get_next_topic_from_plan():
    """
    Selects a random topic from content_plan_india.json that has NOT been used yet.
    """
    topics = load_content_plan()
    if not topics:
        return None
    
    used_topics = get_used_topics()
    available_topics = [t for t in topics if t.get('title') not in used_topics]
    
    if not available_topics:
        print("⚠️ All topics from plan have been used! Generating a trending fallback.")
        return {
            "title": "Aviator Game Strategy 2026: Winning Tricks for India",
            "keyword": "aviator crash game strategy",
            "intent": "commercial",
            "category": "Trending"
        }
        
    selected = random.choice(available_topics)
    print(f"🎯 Selected Topic: {selected.get('title')} (Unused)")
    return selected

def log_to_google_sheet(site_url, topic, status, link, model_used):
    """
    Logs the execution result to Google Sheets using credentials from env.
    """
    try:
        json_creds = os.getenv("GOOGLE_CREDENTIALS")
        if not json_creds:
            print("⚠️ GOOGLE_CREDENTIALS missing. Skipping sheet log.")
            return

        # Parse JSON credentials
        creds_dict = json.loads(json_creds)
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)

        # Open Sheet
        try:
            sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_TAB_NAME)
        except gspread.exceptions.WorksheetNotFound:
            print(f"⚠️ Worksheet '{SHEET_TAB_NAME}' not found. Using first sheet.")
            sheet = client.open_by_key(SHEET_ID).sheet1
        except Exception as e:
            print(f"⚠️ Error opening sheet: {e}")
            return

        # Prepare Row (Standard 11-column structure)
        # 1:Time, 2:Site, 3:Login, 4:Pass, 5:Target, 6:Anchor, 7:Topic, 8:Style, 9:Status, 10:Link, 11:Model
        row = [
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), # 1
            site_url,                                             # 2
            "",                                                   # 3
            "",                                                   # 4
            "",                                                   # 5
            "",                                                   # 6
            topic,                                                # 7
            "",                                                   # 8
            "✅ Success" if status == "success" else "❌ Error",   # 9
            link if link else "N/A",                              # 10
            model_used                                            # 11
        ]
        

        # Append
        sheet.append_row(row)
        print(f"📊 Logged to Google Sheet: {row}")

    except Exception as e:
        print(f"⚠️ Critical error logging to sheet: {e}")

def fetch_tasks_from_sheet(rewrite_mode=False):
    """
    Fetches pending tasks from Google Sheet.
    If rewrite_mode is True, fetches already 'Success' tasks to rewrite them.
    """
    try:
        json_creds = os.getenv("GOOGLE_CREDENTIALS")
        
        # Load Creds (File or Env)
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        if json_creds:
            if os.path.exists(json_creds):
                # If it's a path to a file
                creds = ServiceAccountCredentials.from_json_keyfile_name(json_creds, scope)
            else:
                # If it's the JSON content itself
                try:
                    creds_dict = json.loads(json_creds)
                    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
                except Exception as e:
                    print(f"⚠️ Error parsing GOOGLE_CREDENTIALS JSON: {e}")
                    return []
        else:
             print("⚠️ No Google Credentials found in environment (GOOGLE_CREDENTIALS). Cannot fetch tasks.")
             return []

        client = gspread.authorize(creds)
        
        # Open Sheet
        try:
            sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_TAB_NAME)
        except gspread.exceptions.WorksheetNotFound:
            print(f"⚠️ Worksheet '{SHEET_TAB_NAME}' not found. Trying 'Sheet1'...")
            sheet = client.open_by_key(SHEET_ID).get_worksheet(0)
            

        # Get All Records manually to avoid header issues
        try:
             all_values = sheet.get_all_values()
             if not all_values:
                 return []
                 
             header_row = all_values[0]
             
             # If 'Site URL' not in headers, add them
             if 'Site URL' not in header_row:
                 print("⚠️ No valid headers found. Adding standard headers...")
                 sheet.insert_row(SHEET_HEADERS, 1)
                 all_values = [SHEET_HEADERS] + all_values
                 header_row = SHEET_HEADERS
             
             # Map values to dictionaries using header_row
             records = []
             for i, row in enumerate(all_values[1:]):
                 d = {'row_id': i + 2} # 1-indexed + header
                 for j, header in enumerate(header_row):
                     if j < len(row):
                         d[header if header else f"Col{j}"] = row[j]
                 records.append(d)
                 
        except Exception as e:
             print(f"⚠️ Error reading records: {e}")
             return []

        # Load known sites data for fallback credentials
        known_sites = {}
        try:
            with open('data/sites_data.json', 'r') as f:
                sites_list = json.load(f)
                for s in sites_list:
                    # Normalize URL (strip trailing slash) for matching
                    url = s.get('site_url', '').rstrip('/')
                    known_sites[url] = s
        except Exception as e:
            print(f"⚠️ Could not load sites_data.json for fallback: {e}")

        pending_tasks = []
        
        # Debug: Print columns
        if records:
            print(f"📊 Sheet Columns: {list(records[0].keys())}")
            
        for i, row in enumerate(records):
            status = row.get('Status', '').strip()
            site_url = row.get('Site URL', '').strip()
            topic = row.get('Article Topic', row.get('Topic', '')).strip()
            
            # Logic: 
            # Normal mode: Add if Status is empty or 'Pending'
            # Rewrite mode: Add if Status contains 'Success'
            should_add = False
            if rewrite_mode:
                if "success" in status.lower():
                    should_add = True
            else:
                if (not status or status.lower() == 'pending') and site_url and topic:
                    should_add = True

            if should_add and site_url and topic:
                
                # Fallback to sites_data.json for missing fields
                login = row.get('Login', '').strip()
                password = row.get('App Password', '').strip()
                target_url = row.get('Target Link', row.get('Target URL', '')).strip()
                anchor = row.get('Anchor Text', row.get('Anchor', '')).strip()
                
                # Normalize URL for matching
                def normalize(url):
                    return url.lower().replace("https://", "").replace("http://", "").rstrip("/")

                sheet_url_norm = normalize(site_url)
                
                # Check against known sites
                matched_site_data = None
                for k, v in known_sites.items():
                    if normalize(k) == sheet_url_norm:
                        matched_site_data = v
                        break
                
                if matched_site_data:
                    site_data = matched_site_data
                    if site_data.get('site_url'):
                        site_url = site_data.get('site_url').rstrip('/')
                    if not login:
                        login = site_data.get('login', '')
                    if not password:
                        password = site_data.get('app_password', '')
                    if not target_url:
                        target_url = site_data.get('target_url', '')
                    if not anchor:
                        anchor = site_data.get('anchor', '')  

                task = {
                    "row_id": i + 2, # 1-based index + header
                    "date": row.get('Date', row.get('Time', '')).strip(), # Added Date field
                    "site_url": site_url,
                    "login": login,
                    "app_password": password,
                    "target_url": target_url,
                    "anchor": anchor,
                    "topic": topic,
                    "author_style": row.get('Author Style', 'neutral').strip(),
                    "rewrite": rewrite_mode
                }
                pending_tasks.append(task)
                
        print(f"✅ Found {len(pending_tasks)} tasks to process (Rewrite: {rewrite_mode}).")
        return pending_tasks

    except Exception as e:
        print(f"⚠️ Error fetching tasks from sheet: {e}")
        return []

def update_sheet_status(row_id, status, link, model):
    """
    Updates the specific row in the sheet with the result.
    Matches user sheet: 1:Time, 2:Site, 3:Login, 4:Pass, 5:Target, 6:Anchor, 7:Topic, 8:Style, 9:Status, 10:Link, 11:Model
    """
    try:
        json_creds = os.getenv("GOOGLE_CREDENTIALS")
        if not json_creds:
            print("⚠️ GOOGLE_CREDENTIALS missing. Skipping sheet status update.")
            return

        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        if os.path.exists(json_creds):
            creds = ServiceAccountCredentials.from_json_keyfile_name(json_creds, scope)
        else:
            try:
                creds_dict = json.loads(json_creds)
                creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            except Exception as e:
                print(f"⚠️ Error parsing GOOGLE_CREDENTIALS JSON: {e}")
                return
        client = gspread.authorize(creds)
        
        try:
            sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_TAB_NAME)
        except:
             sheet = client.open_by_key(SHEET_ID).get_worksheet(0)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status_icon = "✅ Success" if status == "success" else "❌ Error"
        
        # Update cells based on user's current sheet structure
        # A=1(Time), I=9(Status), J=10(Link), K=11(Model)
        sheet.update_cell(row_id, 1, timestamp)    # Update interaction time
        sheet.update_cell(row_id, 9, status_icon)  # Actual Status column (I)
        sheet.update_cell(row_id, 10, link if link else "N/A")  # New Post URL (J)
        sheet.update_cell(row_id, 11, model)       # Model Used (K)
        
        print(f"📝 Updated Sheet Row {row_id}: {status} in Col 9")
        
    except Exception as e:
        print(f"⚠️ Error updating sheet row {row_id}: {e}")


def build_seo_title(topic, year=2026):
    """
    Builds an SEO-optimized post title.
    Format: [Topic]: Ultimate Guide & Winning Strategies [Year]
    """
    # Remove year if already in topic
    clean_topic = topic.replace(str(year), '').strip().rstrip(':').strip()
    return f"{clean_topic}: Ultimate Guide & Winning Strategies {year}"


def build_meta_description(topic, anchor_text, year=2026):
    """
    Builds a 155-char SEO meta description.
    """
    desc = f"Master {topic} in {year} with expert insider strategies, RNG patterns, and pro tips for Indian players. Start winning with {anchor_text} today!"
    return desc[:155]


def get_or_create_wp_term(site_url, username, app_password, name, taxonomy='categories'):
    """
    Finds or creates a WordPress category or tag by name.
    Returns the term ID.
    """
    auth_header = base64.b64encode(f"{username}:{app_password}".encode()).decode()
    headers = {'Authorization': f'Basic {auth_header}', 'Content-Type': 'application/json'}
    endpoint = f"{site_url.rstrip('/')}/wp-json/wp/v2/{taxonomy}"
    
    # Search for existing term
    try:
        r = requests.get(endpoint, headers=headers, params={'search': name, 'per_page': 1}, timeout=15)
        if r.status_code == 200 and r.json():
            return r.json()[0]['id']
    except Exception:
        pass
    
    # Create new term if not found
    try:
        r = requests.post(endpoint, headers=headers, json={'name': name}, timeout=15)
        if r.status_code == 201:
            return r.json().get('id')
    except Exception as e:
        print(f"   ⚠️ Failed to create {taxonomy} '{name}': {e}")
    return None


def get_category_for_topic(topic):
    """
    Infers the WordPress category from the topic name.
    """
    topic_lower = topic.lower()
    if any(k in topic_lower for k in ['aviator', 'crash']):
        return 'Aviator'
    if any(k in topic_lower for k in ['1win', 'betway', 'parimatch', 'melbet']):
        return 'Casino Reviews'
    if any(k in topic_lower for k in ['strategy', 'trick', 'hack', 'tips', 'guide', 'win']):
        return 'Strategies'
    if any(k in topic_lower for k in ['bonus', 'promo', 'deposit', 'withdraw', 'upi', 'paytm']):
        return 'Bonuses & Payments'
    if any(k in topic_lower for k in ['cricket', 'ipl', 'bet', 'betting']):
        return 'Cricket Betting'
    if any(k in topic_lower for k in ['teen patti', 'teenpatti', 'patti']):
        return 'Teen Patti'
    if any(k in topic_lower for k in ['rummy', 'card game']):
        return 'Rummy'
    return 'Casino Tips'


def extract_tags_from_topic(topic, keyword=''):
    """
    Generates a list of SEO tags from topic and keyword.
    """
    base_tags = ['India', 'iGaming', '2026', 'Real Money']
    topic_lower = topic.lower()
    if 'cricket' in topic_lower or 'ipl' in topic_lower:
        base_tags += ['Cricket', 'IPL 2026', 'Sports Betting']
    elif 'teen patti' in topic_lower or 'patti' in topic_lower:
        base_tags += ['Teen Patti', 'Card Games', 'Online Gaming']
    elif 'rummy' in topic_lower:
        base_tags += ['Rummy', 'Card Games', 'Online Gaming']
    words = (topic + ' ' + keyword).split()
    for word in words:
        if len(word) > 4 and word not in base_tags:
            base_tags.append(word.strip(',.:'))
    return list(set(base_tags))[:8]  # Max 8 tags


def publish_to_wordpress(site_url, username, app_password, title, content,
                         post_id=None, status='publish', meta_description=None,
                         topic=None, keyword=None):
    # Force HTTPS to prevent 301 redirects to GET (200 OK error)
    if site_url.startswith("http://"):
        print(f"   🔄 Upgrading URL to HTTPS to avoid redirect...")
        site_url = site_url.replace("http://", "https://")

    auth_string = f"{username}:{app_password}"
    auth_header = base64.b64encode(auth_string.encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/json',
        'User-Agent': 'WordPress-Publisher-Bot/1.0'
    }
    
    if post_id:
        endpoint = f"{site_url.rstrip('/')}/wp-json/wp/v2/posts/{post_id}"
        print(f"   🚀 Updating existing post {post_id}...")
    else:
        endpoint = f"{site_url.rstrip('/')}/wp-json/wp/v2/posts"
        print(f"   🚀 Отправка новой статьи в WordPress...")
        
    payload = {
        'title': title,
        'content': content,
        'status': status,
    }

    # Add SEO meta description if provided (Yoast & RankMath)
    if meta_description:
        payload['meta'] = {
            '_yoast_wpseo_metadesc': meta_description,
            'rank_math_description': meta_description,
        }

    # STEP 1 (On-Site SEO): Auto-assign Categories & Tags
    if topic:
        try:
            category_name = get_category_for_topic(topic)
            category_id = get_or_create_wp_term(site_url, auth_header.split(' ')[-1] if ' ' in auth_header else '',
                                                 '', category_name, 'categories')
            if not category_id:
                # Re-try with full auth
                auth_s = f"{username}:{app_password}"
                auth_h = base64.b64encode(auth_s.encode()).decode()
                category_id = get_or_create_wp_term(site_url, username, app_password, category_name, 'categories')
                
            if category_id:
                payload['categories'] = [category_id]
                print(f"   🗂️ Category: {category_name} (ID: {category_id})")

            tag_names = extract_tags_from_topic(topic, keyword or '')
            tag_ids = []
            for tag in tag_names:
                tid = get_or_create_wp_term(site_url, username, app_password, tag, 'tags')
                if tid:
                    tag_ids.append(tid)
            if tag_ids:
                payload['tags'] = tag_ids
                print(f"   🏷️ Tags: {', '.join(tag_names[:5])}...")
        except Exception as e:
            print(f"   ⚠️ Category/tag error: {e}")

    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=45)
        if response.status_code in [200, 201]:
            return response.json()
        print(f"   ❌ Ошибка WordPress: {response.status_code} - {response.text}")
        return None
    except Exception as e:
        print(f"   ❌ Ошибка публикации: {e}")
        return None


def send_telegram_post(title, url, topic):
    """Posts a new article announcement to Telegram channel after successful publish."""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '')
    chat_id   = os.getenv('TELEGRAM_CHAT_ID', '')
    if not bot_token or not chat_id:
        return  # Silently skip if not configured

    # Pick emoji by topic
    topic_lower = topic.lower()
    if 'cricket' in topic_lower or 'ipl' in topic_lower:
        emoji = '\U0001F3CF'
    elif 'teen patti' in topic_lower or 'patti' in topic_lower:
        emoji = '\U0001F3B4'
    elif 'rummy' in topic_lower:
        emoji = '\U0001F0CF'
    elif 'aviator' in topic_lower:
        emoji = '\u2708\uFE0F'
    else:
        emoji = '\U0001F3B0'

    message = (
        f"{emoji} *New Article Published!*\n\n"
        f"*{title}*\n"
        f"\U0001F517 [Read More]({url})\n\n"
        f"\U0001F4CA Get expert tips, strategies & bonuses for Indian players.\n"
        f"\U0001F447 Click the link above to read!"
    )
    try:
        resp = requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            json={
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'Markdown',
                'disable_web_page_preview': False,
            },
            timeout=10
        )
        if resp.status_code == 200:
            print(f"   \u2708\uFE0F Telegram post sent to channel!")
        else:
            print(f"   \u26A0\uFE0F Telegram error: {resp.status_code} {resp.text[:100]}")
    except Exception as e:
        print(f"   \u26A0\uFE0F Telegram exception: {e}")


def generate_faq_block(topic, target_url, anchor):
    """Generates 5 FAQs via Groq and returns HTML accordion + JSON-LD FAQPage schema."""
    groq_key = os.getenv('GROQ_API_KEY', '')
    if not groq_key:
        return ''

    prompt = f"""Generate exactly 5 FAQ items for an article about: "{topic}"

Context: Indian audience, gambling/gaming niche, 2026.
Format your response as JSON array only, no other text:
[
  {{"q": "Question 1?", "a": "Answer 1 (2-3 sentences, practical for Indian players)"}},
  {{"q": "Question 2?", "a": "Answer 2"}},
  {{"q": "Question 3?", "a": "Answer 3"}},
  {{"q": "Question 4?", "a": "Answer 4"}},
  {{"q": "Question 5?", "a": "Answer 5"}}
]"""

    try:
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
            json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "max_tokens": 800, "temperature": 0.6},
            timeout=30
        )
        if resp.status_code != 200:
            return ''

        import json as _json
        raw = resp.json()['choices'][0]['message']['content'].strip()
        # Extract JSON array
        start, end = raw.find('['), raw.rfind(']')
        if start == -1 or end == -1:
            return ''
        faqs = _json.loads(raw[start:end+1])

        # Build HTML accordion
        html = '<div class="faq-section" style="margin:40px 0;">\n'
        html += '<h2 style="color:#facc15;margin-bottom:20px;">\u2753 Frequently Asked Questions</h2>\n'
        html += '<div class="faq-list">\n'
        for faq in faqs:
            q = faq.get('q', '').strip()
            a = faq.get('a', '').strip()
            html += f'<details style="background:rgba(26,29,41,0.8);border:1px solid rgba(255,255,255,0.1);border-radius:8px;padding:15px;margin-bottom:10px;"><summary style="cursor:pointer;font-weight:700;color:#f0c040;">{q}</summary><p style="margin-top:10px;color:#d1d5db;">{a}</p></details>\n'
        html += '</div>\n</div>\n'

        # Build JSON-LD FAQPage schema
        schema_items = [{"@type": "Question", "name": f.get('q'), "acceptedAnswer": {"@type": "Answer", "text": f.get('a')}} for f in faqs]
        schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": schema_items}
        html += f'<script type="application/ld+json">{_json.dumps(schema, ensure_ascii=False)}</script>\n'

        print(f"   \u2753 FAQ block generated ({len(faqs)} questions)")
        return html
    except Exception as e:
        print(f"   \u26A0\uFE0F FAQ generation failed: {e}")
        return ''


def get_recent_wp_posts(site_url, username, app_password, count=5):
    """
    Fetches recently published posts from WordPress to use for internal linking.
    Returns list of dicts with 'title' and 'link'.
    """
    auth_string = f"{username}:{app_password}"
    auth_header = base64.b64encode(auth_string.encode()).decode()
    headers = {'Authorization': f'Basic {auth_header}'}
    endpoint = f"{site_url.rstrip('/')}/wp-json/wp/v2/posts"
    params = {'per_page': count, 'status': 'publish', 'orderby': 'date', 'order': 'desc'}
    try:
        response = requests.get(endpoint, headers=headers, params=params, timeout=30)
        if response.status_code == 200:
            posts = response.json()
            return [{'title': p.get('title', {}).get('rendered', ''), 'link': p.get('link', '')} for p in posts]
    except Exception as e:
        print(f"   ⚠️ Could not fetch recent posts for internal linking: {e}")
    return []

def inject_internal_links(content, related_posts, current_topic):
    """
    Injects internal links to related posts + always adds a cornerstone page link.
    The cornerstone link (/aviator-guide/) builds topical authority.
    """
    if not related_posts and not content:
        return content
    
    # --- Cornerstone link block (always included) ---
    topic_lower = current_topic.lower()
    if 'cricket' in topic_lower or 'ipl' in topic_lower:
        cornerstone_url = 'https://luckybetvip.com/cricket-betting-guide/'
        cornerstone_text = '🏏 Complete Cricket Betting Guide India 2026'
    elif 'teen patti' in topic_lower or 'patti' in topic_lower:
        cornerstone_url = 'https://luckybetvip.com/teen-patti-guide/'
        cornerstone_text = '🃏 Ultimate Teen Patti Real Money Guide 2026'
    elif 'rummy' in topic_lower:
        cornerstone_url = 'https://luckybetvip.com/rummy-guide/'
        cornerstone_text = '🃏 Online Rummy Guide: Win Real Money in India'
    else:
        # Check if topic is a review or strategy
        if 'review' in topic_lower:
            cornerstone_url = 'https://luckybetvip.com/casino-reviews/'
            cornerstone_text = '⭐ Top-Rated Online Casinos in India: 2026 Reviews'
        elif 'strategy' in topic_lower or 'trick' in topic_lower:
            cornerstone_url = 'https://luckybetvip.com/aviator-strategy/'
            cornerstone_text = '📈 Professional Aviator Strategies: Master the Algorithm'
        else:
            cornerstone_url = 'https://luckybetvip.com/aviator-guide/'
            cornerstone_text = '✈️ Complete Aviator Game Guide for India Players'

    cornerstone_html = f'\n<div class="cornerstone-link" style="background:linear-gradient(135deg,#1e293b,#0f172a);border:1px solid #e11d48;border-radius:10px;padding:15px 20px;margin:30px 0;">\n'
    cornerstone_html += f'<p style="margin:0;font-size:1.1rem;"><strong>📖 Read Next:</strong> <a href="{cornerstone_url}" style="color:#facc15;text-decoration:none;" rel="dofollow">{cornerstone_text}</a></p>\n</div>\n'

    if not related_posts:
        return content + cornerstone_html

    # --- Related posts block ---
    filtered = [p for p in related_posts if current_topic.lower()[:20] not in p['title'].lower()]
    
    links_html = '\n<div class="related-posts" style="background:#1a1a2e;border-radius:8px;padding:20px;margin:30px 0;">\n'
    links_html += '<h3 style="color:#e0a000;">📚 Related Articles You May Like</h3>\n<ul style="list-style:none;padding:0;">\n'
    for post in filtered[:4]:
        links_html += f'  <li style="margin:8px 0;">➡️ <a href="{post["link"]}" style="color:#f0c040;">{post["title"]}</a></li>\n'
    links_html += '</ul>\n</div>\n'
    
    # Inject cornerstone near top (after 2nd paragraph), related posts near bottom
    paragraphs = content.split('</p>')
    if len(paragraphs) > 3:
        paragraphs[2] = paragraphs[2] + cornerstone_html
        content = '</p>'.join(paragraphs)
    else:
        content = cornerstone_html + content

    if '</div>' in content:
        last_div = content.rfind('</div>')
        content = content[:last_div] + links_html + content[last_div:]
    else:
        content += links_html
    
    return content

def find_wp_post_id(site_url, username, app_password, title):
    """
    Tries to find the post ID by title.
    """
    auth_string = f"{username}:{app_password}"
    auth_header = base64.b64encode(auth_string.encode()).decode()
    headers = {'Authorization': f'Basic {auth_header}'}
    
    endpoint = f"{site_url.rstrip('/')}/wp-json/wp/v2/posts"
    params = {'search': title, 'per_page': 1}
    
    try:
        response = requests.get(endpoint, headers=headers, params=params, timeout=30)
        if response.status_code == 200:
            posts = response.json()
            if posts and len(posts) > 0:
                # Check if title matches exactly or closely
                found_title = posts[0].get('title', {}).get('rendered', '')
                if title.lower() in found_title.lower() or found_title.lower() in title.lower():
                    return posts[0].get('id')
        return None
    except Exception as e:
        print(f"   ⚠️ Error finding post ID: {e}")
        return None

def generate_article_template(topic, target_link, anchor_text):
    """
    Minimal dynamic template as a last resort. 
    Removed static strategy text to avoid repetition.
    """
    title = f"{topic}: Essential Guide & 2026 Strategy"
    img1 = random.choice(GAMBLING_IMAGES)
    content = f"""
    <h1>Modern Insights: {topic}</h1>
    <div class="post-image"><img src="{img1}" alt="{topic}" style="width:100%; border-radius:8px; margin: 20px 0;"></div>
    
    <p>In the evolving landscape of 2026, <strong>{topic}</strong> remains a focal point for enthusiasts. Understanding the core mechanics and timing is essential for success.</p>
    
    <h2>Strategic Overview</h2>
    <p>Success in this area requires a blend of patience and analytical observation. While many rely on luck, experienced players look for subtle shifts in data patterns.</p>
    
    <h3>Key Takeaways</h3>
    <ul>
        <li>Always stay updated with the latest version of the platform.</li>
        <li>Financial discipline is more important than any single win.</li>
        <li>Utilize tools that provide real-time data analysis.</li>
    </ul>

    <h2>Why Reliability Matters</h2>
    <p>Choosing the right platform is critical. We recommend checking out <a href="{target_link}">{anchor_text}</a> for a secure and verified experience.</p>
    
    <p>Always play responsibly and know when to take a break.</p>
    """
    return title, content

def update_existing_post(site_url, username, app_password, target_url, anchor, topic):
    print(f"   🔍 Поиск релевантных статей для перелинковки по теме '{topic}'...")
    return None

def generate_article(topic, target_link, anchor_text, author_style='neutral', lang='en', use_ai_images=False, use_pseo=False):
    """
    Core content generation engine.
    lang: 'en', 'hi' (Hindi), 'bn' (Bengali), 'te' (Telugu), 'mr' (Marathi)
    """
    # Check if we should override topic from content plan
    planned_content = None
    # If topic is explicitly set to 'random' or placeholder, grab from plan
    if topic == "random" or "{random_india_topic}" in topic:
        planned_content = get_next_topic_from_plan()
    
    # If no plan found (or not requested), stick to original topic
    if planned_content:
        topic = planned_content['title']
        keyword = planned_content.get('keyword', topic)
        intent = planned_content.get('intent', 'informational')
        category = planned_content.get('category', 'General')
        print(f"🎲 Selected Random Topic: [{category}] {topic} (Intent: {intent})")
        
        # Enhanced Prompt for Indian Niche (English Only) - VERSION 6.0 (SEO-Schema)
        # Language Configuration
        lang_config = {
            'hi': ("Hindi (Devanagari script)", "Write in Hindi (Devanagari). Keep technical terms in English."),
            'bn': ("Bengali", "Write in Bengali script. Keep technical terms in English."),
            'te': ("Telugu", "Write in Telugu script. Keep technical terms in English."),
            'mr': ("Marathi", "Write in Marathi (Devanagari) script. Keep technical terms in English."),
            'ta': ("Tamil", "Write in Tamil script. Keep technical terms in English."),
            'en': (None, "Write in English with an Indian cultural context.")
        }
        
        # SEO Freshness: Update title with Month / Year
        topic = get_updated_title(topic, lang=lang)
        
        # pSEO Injection: Add City if requested
        if use_pseo:
            city = get_random_indian_city()
            topic = f"{topic} in {city}"
            print(f"📍 pSEO Active: Targeting {city}...")
        
        lang_name, lang_req = lang_config.get(lang, lang_config['en'])
        
        if lang != 'en':
            role = f"You are an elite iGaming analyst and insider for the Indian market, writing in {lang_name}."
        else:
            role = f"You are an elite iGaming analyst and insider for the Indian market. {STYLE_PROMPTS.get(author_style, STYLE_PROMPTS['neutral'])}"

        prompt = f"""
        {role}
        
        Task: Write a MASSIVE, comprehensive, and high-converting SEO article in HTML format.
        Language Requirement: {lang_req}
        Topic: {topic}
        Main Keyword: {keyword}
        User Intent: {intent} (Users want SECRETS, HACKS, and WINNING TRICKS).
        Target Audience: Indian players (use ₹, mention UPI/Paytm, use specific local context).

        # HTML FORMATTING RULES (STRICT):
        1. **Hero Section**: Start the article with a <div class="hero-section"> containing a <span class="hero-badge">NEW: Insider Guide</span>, 
           the H1, and a 2-sentence emotional hook.
        2. **Glassmorphism**: Wrap the "Insider Secrets" or "Strategies" section in a <div class="glass-card"> container.
        3. Wrap every strategy in a <div class='strategy-card'>.
        4. Use 🎯 emoji for 'Key Aspects'.
        5. Format Pros/Cons using: <div class='grid-pc'><div class='p'><h4>Pros</h4><ul><li>Pro 1</li></ul></div><div class='c'><h4>Cons</h4><ul><li>Con 1</li></ul></div></div>.
        6. ALL images must have unique, descriptive ALT text related to the topic (e.g., alt="Aviator game strategy India 2026").

        Structure Requirements (Critical - MUST FOLLOW):
        1. Length: **EXTREME PRIORITY - Minimum 3000 words**. This MUST be a long-form authority guide.
        2. **E-E-A-T & Personal Experience**: Google rewards content with first-hand experience. Throughout the article, 
           use phrases like "I tested this...", "In my session with 5,000 INR...", "After 200 rounds, I observed...". 
           Include specific data points and real-life scenarios to prove this isn't just generic AI text.
        3. **Insider Insights: Algorithm Analysis**: Include a massive section titled "Insider Secrets: Algorithm Analysis".
           - Discuss "RNG patterns" and hidden cycles.
           - Mention specific "Signals" (e.g., "The Double-Pink Strategy", "Blue Streak Recovery").
           - Use local Indian gambling terminology (e.g., "khowa", "patti", "chal") to build trust.
           - Make it sound exclusive, expert-level, and backed by "community data".
        4. Use an engaging <h1> tag.
        5. Use at least 15-20 <h2> subheadings and 10-15 <h3> subheadings.
        6. Include a "FAQ" section at the end with 10+ questions and answers.
        7. **SEO Schema - CRITICAL**: After the FAQ section, add a valid JSON-LD FAQ Schema block:
           ```html
           <script type="application/ld+json">
           {{
             "@context": "https://schema.org",
             "@type": "FAQPage",
             "mainEntity": [
               {{
                 "@type": "Question",
                 "name": "[FAQ Question 1 about {topic}]",
                 "acceptedAnswer": {{
                   "@type": "Answer",
                   "text": "[Answer 1]"
                 }}
               }},
               {{
                 "@type": "Question",
                 "name": "[FAQ Question 2 about {topic}]",
                 "acceptedAnswer": {{
                   "@type": "Answer",
                   "text": "[Answer 2]"
                 }}
               }}
             ]
           }}
           </script>
           ```
           Fill in at least 5 real FAQ questions and answers from the article.
        7. **Affiliate Integration**:
           - Use the localized link `/go/1xbet` for all text links with anchor "{anchor_text}".
           - **PROMO CODE**: Explicitly mention the promo code `1x_4393603` throughout the article.
           - **BENEFITS**: Stress that this promo code gives an increased registration bonus, has unlimited validity, and can be shared with friends.
           - **CRITICAL**: After the Winning Strategies section, insert: `[play_1xbet]`
           - **CRITICAL**: At the very end, insert: `[play_1xbet]`
        
        Format Requirement: Return ONLY valid HTML code. No <html> or <body> tags. No markdown blocks.
        """
    else:
        # FALLBACK: If planned_content is None but we had a placeholder, FORCE a fallback topic
        if "{random_india_topic}" in topic or topic == "random":
             topic = "Aviator Game India: 2026 Winning Strategy"
             print(f"⚠️ Placeholder detected but no plan found. Using Fallback Topic: {topic}")

        # pSEO Injection: Add City if requested
        if use_pseo:
            city = get_random_indian_city()
            topic = f"{topic} in {city}"
            print(f"📍 pSEO Active (Fallback path): Targeting {city}...")

        print(f"Generating content (Style: {author_style}) for topic: {topic}")
        style_instruction = STYLE_PROMPTS.get(author_style, STYLE_PROMPTS['neutral'])
        lang_config = {
            'hi': ("Hindi (Devanagari)", "Write in Hindi. Keep tech terms in English."),
            'bn': ("Bengali", "Write in Bengali. Keep tech terms in English."),
            'te': ("Telugu", "Write in Telugu. Keep tech terms in English."),
            'mr': ("Marathi", "Write in Marathi. Keep tech terms in English."),
            'en': (None, "Write in English for the Indian market.")
        }
        lang_name, lang_req = lang_config.get(lang, lang_config['en'])

        if lang != 'en':
            role = f"You are a professional iGaming blog writer for the Indian market, writing in {lang_name}. {style_instruction}"
        else:
            role = f"You are a professional iGaming blog writer for the Indian market. {style_instruction}"

        prompt = f"""
        {role}
        Task: Write a VERY LONG, comprehensive SEO-optimized article in HTML format.
        Language Requirement: {lang_req}
        Topic: {topic}
        Target Audience: Indian players (use INR, UPI, India-specific examples).
        
        CRITICAL REQUIREMENTS — you MUST satisfy ALL of them:
        1. **BRAND FOCUS**: The article must be written under the **1xBet** brand umbrella.
        2. **PROMO CODE**: Integrate the promo code `1x_4393603` naturally. Explain that using this code during registration grants an **increased welcome bonus**.
        3. **LENGTH**: **Minimum 3000 words** — do NOT produce a short article. Expand every section with real examples,
           data tables, step-by-step guides, and pro tips. Write until you reach at least 3000 words.
        4. **E-E-A-T & Personal Experience**: Use first-person narrative ("I tested this 1xBet strategy...", "My results with 5000 INR..."). 
           Include specific percentages, multipliers, and numbers to simulate real expert testing.
        5. SECTIONS: Include at least 12 H2/H3 sections with these types:
           - Introduction (why 1xBet is the top choice for Indians in 2026)
           - Expert Insights: Why {topic} is trending in 2026
           - How It Works (detailed mechanics)
           - Step-by-Step Guide for 1xBet players (at least 7 steps)
           - Winning Strategies (at least 5 specific strategies)
           - Insider Tips & Secrets (real practical hacks)
           - Mistakes to Avoid (at least 5 common mistakes)
           - Why use Promo Code `1x_4393603` (Increased bonus, unlimited validity, shares with friends)
           - Best 1xBet Games in India (mini-table with columns: Game, Type, Min Bet, UPI Support)
           - Risk Management (bankroll, limits)
           - Conclusion
        6. TABLES: Include at least 2 HTML tables with real data.
        7. LINK: Include a natural affiliate link to "{target_link}" with anchor text "{anchor_text}".
        8. SHORTCODES: Insert `[play_1xbet]` after "Winning Strategies" AND at the very end.
        9. Return ONLY clean HTML (h1-h3, p, ul, ol, table, strong, em, div, span). No <html>/<body> tags. No markdown.
        10. **Modern UI Elements**: Use <div class="glass-card"> for important sections and <span class="hero-badge"> for shoutouts.
        11. **Hero Section**: Start with a <div class="hero-section text-center"><span class="hero-badge">2026 Updated</span><h1>{topic}</h1><p class="lead">Insider 1xBet insights for Indian players...</p></div>
        """
    
    # Raw HTTP Request to bypass library issues
    # gemini-2.0-flash returned 429, meaning it exists!
    gemini_key = os.getenv('GEMINI_API_KEY', '').strip()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_key}"

    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            print(f"   🤖 Attempt {attempt+1}/{max_attempts} calling Gemini...")
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                try:
                    content = result['candidates'][0]['content']['parts'][0]['text']
                    content = content.replace('```html', '').replace('```', '')
                    
                    # INJECT IMAGES LOGIC - unique images (no duplicates)
                    try:
                         picked = []
                         if use_ai_images:
                             ai_img = generate_ai_image(topic)
                             if ai_img: picked.append(ai_img)
                         
                         if len(picked) < 2:
                             # Fill remaining or all with stock
                             available = list(set(GAMBLING_IMAGES))
                             to_pick = 2 - len(picked)
                             picked.extend(random.sample(available, min(to_pick, len(available))))

                         parts = content.split('</p>')
                         if len(parts) > 2:
                             img_html1 = f'<div class="post-image" style="margin: 20px 0;"><img src="{picked[0]}" alt="{topic} India" style="width:100%; border-radius:8px;" loading="lazy"></div>'
                             parts[1] = parts[1] + img_html1
                         if len(parts) > 5 and len(picked) > 1:
                             img_html2 = f'<div class="post-image" style="margin: 20px 0;"><img src="{picked[1]}" alt="Casino strategy {topic}" style="width:100%; border-radius:8px;" loading="lazy"></div>'
                             parts[4] = parts[4] + img_html2
                         content = '</p>'.join(parts)
                         
                         # SEO Injection: Dynamic Table, WhatsApp CTA & Calculator
                         content = content.replace('</h1>', f'</h1>{generate_dynamic_aviator_table()}', 1)
                         
                         # Inject WhatsApp CTA in the middle (after 3rd paragraph if possible)
                         if len(parts) > 3:
                             content = content.replace('</p>', f'</p>{generate_whatsapp_cta(topic)}', 3)
                         if '<h2>Conclusion</h2>' in content:
                             content = content.replace('<h2>Conclusion</h2>', f'{generate_calculator_html()}<h2>Conclusion</h2>', 1)
                         else:
                             content += generate_calculator_html()
                             
                    except Exception as img_err:
                        print(f'⚠️ Image injection failed: {img_err}')

                    # --- SEO SCHEMA INJECTION (Gemini) ---
                    schema_html = generate_game_schema()
                    faq_pairs = [
                       ("Is Aviator game legal in India?", "Yes, it is legal to play on international licensed platforms."),
                       ("What is the minimum deposit?", "The minimum deposit varies by site but usually starts from ₹300-500.")
                    ]
                    schema_html += generate_faq_schema(faq_pairs)
                    schema_html += generate_review_schema(topic)
                    content += f"\n\n{schema_html}"

                    return topic, content, "gemini-2.0-flash (Raw HTTP)"
                except (KeyError, IndexError) as e:
                    print(f"⚠️ API Response Parsing Error: {e}. Body: {result}")
                    raise ValueError("Invalid API response structure")
            elif response.status_code == 429:
                # Exponential backoff for 429
                wait_time = min(60 * (2 ** (attempt // 2)), 300) 
                print(f"   ⏳ Rate Limited (429). Waiting {wait_time}s...")
                time.sleep(wait_time)
                continue
            else:
                print(f"⚠️ API Error {response.status_code}: {response.text}")
                # For some errors, waiting might help, for others (400) it won't.
                time.sleep(10)
                continue
                
        except Exception as e:
            print(f"⚠️ Generation error: {e}.")
            if attempt == max_attempts - 1:
                print("❌ All attempts failed. Skipping content generation.")
                return None, None, None
            time.sleep(10)
            
    # --- GROQ FALLBACK: Gemini failed all retries, try Groq ---
    print("⚡ Gemini exhausted all retries. Trying Groq API fallback...")
    return generate_with_groq(prompt, topic, use_ai_images=use_ai_images)


def generate_with_groq(prompt, topic, use_ai_images=False):
    """
    Fallback content generation using Groq API (llama-3.3-70b-versatile).
    Fast, free, and generous rate limits (30 req/min).
    Set GROQ_API_KEY in your .env to enable.
    """
    groq_key = os.getenv('GROQ_API_KEY', '').strip()
    if not groq_key:
        print("   ⚠️ GROQ_API_KEY not set. Skipping Groq fallback.")
        return None, None, None

    print("   🚀 Switching to Groq API (llama-3.3-70b-versatile)...")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        'Authorization': f'Bearer {groq_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are an elite iGaming SEO expert. Always respond with valid HTML only, no markdown."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 8000,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            content = content.replace('```html', '').replace('```', '').strip()
            
            # Inject 2 UNIQUE images (random.sample prevents duplicates)
            try:
                picked = []
                if use_ai_images:
                    ai_img = generate_ai_image(topic)
                    if ai_img: picked.append(ai_img)
                
                if len(picked) < 2:
                    available = list(set(GAMBLING_IMAGES))
                    to_pick = 2 - len(picked)
                    picked.extend(random.sample(available, min(to_pick, len(available))))

                parts = content.split('</p>')
                if len(parts) > 2:
                    parts[1] += f'<div class="post-image" style="margin:20px 0;"><img src="{picked[0]}" alt="{topic} India" style="width:100%;border-radius:8px;" loading="lazy"></div>'
                if len(parts) > 4 and len(picked) > 1:
                    parts[min(4, len(parts)-2)] += f'<div class="post-image" style="margin:20px 0;"><img src="{picked[1]}" alt="Casino tips {topic}" style="width:100%;border-radius:8px;" loading="lazy"></div>'
                content = '</p>'.join(parts)
                
            except Exception as e:
                print(f"⚠️ Image injection failed: {e}")

            # SEO Injection (Groq path)
            content = content.replace('</h1>', f'</h1>{generate_dynamic_aviator_table()}', 1)
            parts = content.split('</p>')
            if len(parts) > 3:
                 content = content.replace('</p>', f'</p>{generate_whatsapp_cta(topic)}', 3)
            
            if '<h2>Conclusion</h2>' in content:
                content = content.replace('<h2>Conclusion</h2>', f'{generate_calculator_html()}<h2>Conclusion</h2>', 1)
            else:
                content += generate_calculator_html()
            
            # --- SEO SCHEMA INJECTION (Groq) ---
            schema_html = generate_game_schema()
            faq_pairs = [
                ("Is Aviator game legal in India?", "Yes, it is legal to play on international licensed platforms like 1Win."),
                ("Can I withdraw in INR?", "Yes, you can withdraw your winnings via UPI, Paytm, and local bank transfer.")
            ]
            schema_html += generate_faq_schema(faq_pairs)
            schema_html += generate_review_schema(topic)
            content += f"\n\n{schema_html}"

            print(f"   ✅ Groq generated content ({len(content)} chars)")
            return topic, content, "groq-llama3.3-70b"
        else:
            print(f"   ❌ Groq Error {response.status_code}: {response.text[:200]}")
            return None, None, None
    except Exception as e:
        print(f"   ❌ Groq request failed: {e}")
        return None, None, None



def run_tasks(data=None, output_file='results.json', rewrite_mode=False, max_tasks=1, lang='en', use_ai_images=False, use_pseo=False):
    """Run publishing tasks. max_tasks limits how many articles to publish per run."""
    # If no data provided, fetch from sheet
    if not data:
        print(f"📥 Fetching tasks from Google Sheet (Rewrite Mode: {rewrite_mode})...")
        data = fetch_tasks_from_sheet(rewrite_mode=rewrite_mode)
        
    if not data:
        print("ℹ️ No pending tasks found.")
        return []
        
    results = []
    published_count = 0
    for i, task in enumerate(data):
        if max_tasks and published_count >= max_tasks:
            print(f"\n✅ Reached daily limit of {max_tasks} article(s). Stopping.")
            break
        print(f"\n--- Task {i+1} ---")
        site_url = task.get('site_url')
        login = task.get('login')
        password = task.get('app_password')
        target_url = task.get('target_links', task.get('target_url')) 
        anchor = task.get('anchor_text', task.get('anchor'))
        topic = task.get('article_topic', task.get('topic'))
        style = task.get('author_style', 'neutral')
        row_id = task.get('row_id') # Row ID for sheet update
        is_rewrite = task.get('rewrite', rewrite_mode)
        
        if not all([site_url, login, password, target_url, anchor, topic]):
            print(f"Skip task {i+1}: Missing fields.")
            continue
            
        # --- DATE SCHEDULING LOGIC ---
        task_date_str = task.get('date', '').strip()
        if task_date_str:
            try:
                # Handle YYYY-MM-DD or DD.MM.YYYY
                if '.' in task_date_str:
                    task_date = datetime.datetime.strptime(task_date_str, "%d.%m.%Y").date()
                else:
                    task_date = datetime.datetime.strptime(task_date_str, "%Y-%m-%d").date()
                
                today = datetime.date.today()
                if task_date > today:
                    print(f"⏳ Task {i+1} scheduled for {task_date_str}. Skipping (future date).")
                    continue
            except ValueError:
                print(f"⚠️ Task {i+1} has invalid date format: {task_date_str}. Processing anyway.")
        # -----------------------------
        # Generator now returns model name too
        title, content, model_used = generate_article(topic, target_url, anchor, style, lang=lang, use_ai_images=use_ai_images, use_pseo=use_pseo)
        
        if not content:
            print(f"⚠️ Generation failed for {topic}. Skipping task.")
            if row_id:
                update_sheet_status(row_id, "error", "Generation Failed", "N/A")
            continue

        post_id = None
        if is_rewrite:
            print(f"🔍 Searching for existing post ID for '{title}' on {site_url}...")
            post_id = find_wp_post_id(site_url, login, password, title)
            if not post_id:
                print(f"⚠️ Could not find exact post ID. Publishing as new.")

        # STEP 2: Inject Internal Links (SEO)
        print(f"🔗 Fetching recent posts for internal linking...")
        recent_posts = get_recent_wp_posts(site_url, login, password, count=6)
        if recent_posts:
            content = inject_internal_links(content, recent_posts, topic)
            print(f"   ✅ Internal links injected ({len(recent_posts)} posts found).")
        else:
            print(f"   ℹ️ No existing posts found for internal linking.")

        # STEP 2b: Generate & inject FAQ block (5 FAQs + FAQPage JSON-LD schema)
        faq_block = generate_faq_block(topic, target_url, anchor)
        if faq_block:
            content = content + faq_block

        print(f"Publishing to {site_url}...")
        
        # STEP 3: Build SEO Title & Meta Description
        seo_title = build_seo_title(topic)
        meta_desc = build_meta_description(topic, anchor)
        print(f"   🏷️ SEO Title: {seo_title}")
        
        # publish_to_wordpress now handles both new and updates, plus categories/tags
        post_result = publish_to_wordpress(
            site_url, login, password, seo_title, content,
            post_id=post_id,
            meta_description=meta_desc,
            topic=topic,
            keyword=task.get('keyword', topic)
        )
        
        status = "success" if post_result else "error"
        link = post_result.get('link') if post_result else None
        
        # UPDATE SHEET IF ROW ID EXISTS
        if row_id:
            update_sheet_status(row_id, status, link if link else "N/A", model_used)
        else:
            log_to_google_sheet(site_url, topic, status, link, model_used)
        
        task_result = {
            "site": site_url,
            "status": status,
            "new_post_url": link,
            "is_rewrite": is_rewrite
        }
        results.append(task_result)
        if status == "success":
            published_count += 1
            # Auto-post to Telegram channel
            if link:
                send_telegram_post(seo_title if 'seo_title' in dir() else topic, link, topic)
                # 🚀 SEO: Notify Google Indexing API
                submit_to_google_indexing(link)
                # 🔔 Web Push: Notify OneSignal
                trigger_onesignal_notification(seo_title if 'seo_title' in dir() else topic, link)
        
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    return results

if __name__ == "__main__":
    # Check for flags
    rewrite = "--rewrite" in sys.argv
    use_ai_images = "--ai-images" in sys.argv
    
    # Language detection
    lang = 'en'
    if "--hindi" in sys.argv: lang = 'hi'
    elif "--bengali" in sys.argv: lang = 'bn'
    elif "--telugu" in sys.argv: lang = 'te'
    elif "--marathi" in sys.argv: lang = 'mr'
    
    # --limit N: how many articles to publish per run (default: 1)
    max_per_run = 1
    if "--limit" in sys.argv:
        try:
            idx = sys.argv.index("--limit")
            max_per_run = int(sys.argv[idx + 1])
        except (IndexError, ValueError):
            max_per_run = 1
    
    # If JSON argument provided, use it (Legacy Mode)
    json_input = None
    for arg in sys.argv[1:]:
        if arg.endswith('.json'):
            json_input = arg
            break
            
    if json_input:
        try:
            with open(json_input, 'r') as f:
                user_input = json.load(f)
            run_tasks(user_input, rewrite_mode=rewrite, max_tasks=max_per_run, lang=lang, use_ai_images=use_ai_images)
        except Exception as e:
             print(f"Error reading input file: {e}")
    else:
        # Default mode: Fetch from Sheet, publish 1 article per run
        if lang != 'en':
            print(f"🇮🇳 Multi-GEO Mode: Language set to {lang.upper()}.")
        if use_ai_images:
            print("🎨 AI Image Generation Enabled: Using DALL-E 3 for unique visuals.")
        use_pseo = "--pseo" in sys.argv
        if use_pseo:
            print("📍 pSEO Mode Enabled: Injecting city-specific targeting.")
        run_tasks(rewrite_mode=rewrite, max_tasks=max_per_run, lang=lang, use_ai_images=use_ai_images, use_pseo=use_pseo)


# ----------------------------------------------------------------
# HINDI ARTICLE GENERATION
# Generates a Hindi version of any English article via Groq
# Usage: python3 publish_post.py --hindi
# ----------------------------------------------------------------

def generate_hindi_article(english_topic, english_content, target_url, anchor):
    """
    Translates & rewrites the article in Hindi using Groq.
    Returns (hindi_title, hindi_content).
    """
    groq_key = os.getenv('GROQ_API_KEY', '')
    if not groq_key:
        print("   ⚠️ No GROQ_API_KEY found for Hindi translation")
        return None, None

    hindi_prompt = f"""You are an expert Hindi content writer for Indian gambling/casino audiences.

Rewrite and translate the following article into Hindi (Devanagari script).
Make it natural and engaging for Indian readers aged 18-35.
Keep all HTML tags intact. Keep URLs, numbers, and proper nouns in English.
Include relevant Hindi gambling terms (जीत, कैसीनो, शर्त, bonus, ऑनलाइन गेम).

Target affiliate link to include naturally: <a href="{target_url}" rel="nofollow sponsored">{anchor}</a>
Hindi Title should be compelling — translate the original topic: "{english_topic}"

ENGLISH ARTICLE TO TRANSLATE:
{english_content[:4000]}

Return: First line = Hindi title (no markup), then blank line, then full HTML article in Hindi."""

    try:
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": hindi_prompt}],
                "max_tokens": 4000,
                "temperature": 0.7
            },
            timeout=60
        )
        if resp.status_code == 200:
            text = resp.json()['choices'][0]['message']['content'].strip()
            lines = text.split('\n', 2)
            hindi_title = lines[0].strip()
            hindi_content = '\n'.join(lines[2:]).strip() if len(lines) > 2 else text
            print(f"   ✅ Hindi article generated ({len(hindi_content)} chars)")
            return hindi_title, hindi_content
        else:
            print(f"   ❌ Groq Hindi error: {resp.status_code} {resp.text[:200]}")
            return None, None
    except Exception as e:
        print(f"   ❌ Hindi generation exception: {e}")
        return None, None


def run_hindi_tasks():
    """
    Fetches all Success rows from Google Sheet and publishes Hindi versions.
    Only publishes 1 Hindi article per run to match daily limit.
    """
    print("🇮🇳 Hindi Mode: Generating Hindi versions of published articles...")
    data = fetch_tasks_from_sheet(rewrite_mode=True)   # Reuse Success rows
    if not data:
        print("ℹ️ No success articles found to translate.")
        return

    for task in data[:1]:   # Only 1 per day
        site_url = task.get('site_url')
        login    = task.get('login')
        password = task.get('app_password')
        target   = task.get('target_links', task.get('target_url'))
        anchor   = task.get('anchor_text', task.get('anchor'))
        topic    = task.get('article_topic', task.get('topic'))
        style    = task.get('author_style', 'neutral')

        print(f"\n--- Hindi Task: {topic} ---")
        # First generate English content, then translate
        en_title, en_content, model = generate_article(topic, target, anchor, style)
        if not en_content:
            print("   ⚠️ Could not generate English base. Skipping.")
            continue

        hindi_title, hindi_content = generate_hindi_article(topic, en_content, target, anchor)
        if not hindi_content:
            continue

        # Publish Hindi article — add (Hindi) suffix to distinguish
        full_title = f"{hindi_title} | {topic}"
        link, post_id = publish_to_wordpress(
            site_url, login, password, full_title, hindi_content,
            status='private', meta_description=f"Hindi guide: {topic} - Tips for Indian players"
        )
        if link:
            print(f"   ✅ Hindi article published: {link}")
        else:
            print("   ❌ Failed to publish Hindi article")
