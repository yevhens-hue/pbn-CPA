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
from indexing_api import submit_to_google_indexing

# Google Sheets Imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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

# Stock Images for Injection (Aviator/Gambling/India Theme)
GAMBLING_IMAGES = [
    "https://images.unsplash.com/photo-1605870445919-838d190e8e1e?auto=format&fit=crop&w=1200&q=80", # Poker Chips
    "https://images.unsplash.com/photo-1596838132731-3301c3fd4317?auto=format&fit=crop&w=1200&q=80", # Casino Lights
    "https://images.unsplash.com/photo-1518133910546-b6c2fb7d79e3?auto=format&fit=crop&w=1200&q=80", # Cards
    "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=1200&q=80", # Gaming Setup
    "https://plus.unsplash.com/premium_photo-1676618539992-21c7d3b6df0f?auto=format&fit=crop&w=1200&q=80", # Money/Currency
]

# Prompts are now strictly English + Indian Context
STYLE_PROMPTS = {
    "expert": "Write in a dry, analytical, and technical style. Use professional terminology, data, and deep analysis. Minimal emotion, maximum facts.",
    "lifestyle": "Write in an emotional, easy-going, and accessible style. Use personal examples, storytelling, and address the reader as 'you'. It should feel like a personal blog post.",
    "neutral": "Write in a standard informational style typical of a news portal. Objective and balanced."
}

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

        # Handle case where GOOGLE_CREDENTIALS is a filename instead of a JSON string
        if json_creds.endswith('.json') and os.path.exists(json_creds):
            with open(json_creds, 'r') as f:
                creds_dict = json.load(f)
        elif os.path.exists(os.path.join("PBN_Automation_Final", json_creds)):
             with open(os.path.join("PBN_Automation_Final", json_creds), 'r') as f:
                creds_dict = json.load(f)
        else:
            try:
                creds_dict = json.loads(json_creds)
            except json.JSONDecodeError:
                print(f"⚠️ GOOGLE_CREDENTIALS is neither a valid JSON string nor a found file: {json_creds}")
                return

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

        # Prepare Row
        row = [
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            site_url,
            topic,
            link if link else "N/A",
            "✅ Success" if status == "success" else "❌ Error",
            model_used
        ]
        

        # Append
        sheet.append_row(row)
        print(f"📊 Logged to Google Sheet: {row}")

    except Exception as e:
        print(f"⚠️ Critical error logging to sheet: {e}")

def fetch_tasks_from_sheet():
    """
    Fetches pending tasks from Google Sheet (Tab: 'Report' or 'PBN Sites').
    Returns a list of task dicts.
    """
    try:
        json_creds = os.getenv("GOOGLE_CREDENTIALS")
        creds_file = "scraper-483621-3ae386cecfc1.json"
        
        # Load Creds (File or Env)
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        if os.path.exists(creds_file):
             creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
        elif json_creds:
             creds_dict = json.loads(json_creds)
             creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        else:
             print("⚠️ No Google Credentials found (File or Env). Cannot fetch tasks.")
             return []

        client = gspread.authorize(creds)
        
        # Open Sheet
        try:
            # Try 'Report' tab first (as per config), fallback to first sheet
            sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_TAB_NAME)
        except gspread.exceptions.WorksheetNotFound:
            print(f"⚠️ Worksheet '{SHEET_TAB_NAME}' not found. Trying 'Sheet1'...")
            sheet = client.open_by_key(SHEET_ID).get_worksheet(0)
            

        # Get All Records
        try:
             all_values = sheet.get_all_values()
             if not all_values:
                 return []
                 
             header_row = all_values[0]
             # Clean headers: remove spaces and handle empties
             cleaned_headers = [h.strip() if h.strip() else f"Column_{i}" for i, h in enumerate(header_row)]
             
             # Fallback: if 'Site URL' is missing, it's malformed
             if 'Site URL' not in cleaned_headers:
                  print("⚠️ 'Site URL' not found in headers. Adding standard headers...")
                  expected_headers = ['Date', 'Site URL', 'Login', 'App Password', 'Target Link', 'Anchor Text', 'Topic', 'Author Style', 'Status']
                  sheet.insert_row(expected_headers, 1)
                  # Re-fetch
                  all_values = sheet.get_all_values()
                  cleaned_headers = expected_headers
                  data_rows = all_values[1:] # if we inserted a row, old header is now data? No, insert_row pushes down.
                  # Re-fetch everything to be safe
                  all_values = sheet.get_all_values()
                  cleaned_headers = all_values[0]
                  data_rows = all_values[1:]
             else:
                  data_rows = all_values[1:]

             records = []
             for row in data_rows:
                 record = {}
                 for i, header in enumerate(cleaned_headers):
                     if i < len(row):
                         record[header] = row[i]
                     else:
                         record[header] = ""
                 records.append(record)
                  
        except Exception as e:
             # Fallback if headers are duplicate or empty
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
            # Adjust column names based on user's sheet structure (guessed or standard)
            # We need: Site URL, Article Topic, Target Link, Anchor Text, Status
            
            status = row.get('Status', '').strip()
            site_url = row.get('Site URL', '').strip()
            topic = row.get('Article Topic', row.get('Topic', '')).strip()
            
            # Logic: If Status is empty or 'Pending', add to tasks
            if (not status or status.lower() == 'pending') and site_url and topic:
                
                # Fallback to sites_data.json for missing fields
                login = row.get('Login', '').strip()
                password = row.get('App Password', '').strip()
                target_url = row.get('Target Link', '').strip()
                anchor = row.get('Anchor Text', '').strip()
                
                # Normalize URL for matching (remove protocol and trailing slash)
                # This ensures http://foo.com matches https://foo.com in config
                def normalize(url):
                    return url.lower().replace("https://", "").replace("http://", "").rstrip("/")

                sheet_url_norm = normalize(site_url)
                
                # Check against known sites (normalized keys)
                matched_site_data = None
                for k, v in known_sites.items():
                    if normalize(k) == sheet_url_norm:
                        matched_site_data = v
                        break
                
                if matched_site_data:
                    site_data = matched_site_data
                    # Use canonical URL (to force https if configured)
                    if site_data.get('site_url'):
                        site_url = site_data.get('site_url').rstrip('/')
                        
                    if not login:
                        login = site_data.get('login', '')
                        print(f"🔑 Using cached login for {site_url}")
                    if not password:
                        password = site_data.get('app_password', '')
                        print(f"🔑 Using cached password for {site_url}")
                    if not target_url:
                        target_url = site_data.get('target_url', '')
                        print(f"🔗 Using cached target_link for {site_url}")
                    if not anchor:
                        anchor = site_data.get('anchor', '')  
                        print(f"⚓ Using cached anchor for {site_url}")

                    task = {
                        "row_id": i + 2, # 1-based index + header
                        "date": row.get('Date', row.get('Time', '')).strip(), # Added Date field
                        "site_url": site_url,
                        "login": login,
                        "app_password": password,
                        "target_url": target_url,
                        "anchor": anchor,
                        "topic": topic,
                        "author_style": row.get('Author Style', 'neutral').strip()
                    }
                pending_tasks.append(task)
                
        print(f"✅ Found {len(pending_tasks)} pending tasks in sheet.")
        return pending_tasks

    except Exception as e:
        print(f"⚠️ Error fetching tasks from sheet: {e}")
        return []

def update_sheet_status(row_id, status, link, model):
    """
    Updates the specific row in the sheet with the result.
    """
    try:
        creds_file = "scraper-483621-3ae386cecfc1.json"
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
        client = gspread.authorize(creds)
        
        try:
            sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_TAB_NAME)
        except:
             sheet = client.open_by_key(SHEET_ID).get_worksheet(0)

        # Update columns (assuming Status is col 5, Link col 4 - need to be dynamic or fixed)
        # Better: use cell updates if we know column letters, or find cell by header.
        # For simplicity, assuming standard columns: 
        # Date(1), Site(2), Topic(3), Link(4), Status(5), Model(6)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Update specific cells for that row
        # Note: gspread uses (row, col) 1-based
        # Based on actual headers: 
        # Date(1), Site(2), Login(3), Pass(4), Target(5), Anchor(6), Topic(7), Style(8), Status(9)
        # We want to update: Status(9).
        # And we can add Link(10) and Model(11) as extra info.
        
        # sheet.update_cell(row_id, 1, timestamp) # DO NOT OVERWRITE SCHEDULE DATE
        sheet.update_cell(row_id, 9, "✅ Success" if status == "success" else "❌ Error") # Status (Col 9)
        
        sheet.update_cell(row_id, 10, link if link else "N/A")  # Result Link (Col 10)
        sheet.update_cell(row_id, 11, model)                    # Model Used (Col 11)
        
        print(f"📝 Updated Sheet Row {row_id} (Status=Col 9): {status}")
        
    except Exception as e:
        print(f"⚠️ Error updating sheet row {row_id}: {e}")

def publish_to_wordpress(site_url, username, app_password, title, content, status='publish'):
    # Force HTTPS to prevent 301 redirects to GET (200 OK error)
    if site_url.startswith("http://"):
        print(f"   🔄 Upgrading URL to HTTPS to avoid redirect...")
        site_url = site_url.replace("http://", "https://")

    # Clean credentials to prevent 401 Unauthorized errors
    clean_username = username.strip()
    clean_password = app_password.strip()
    
    auth_string = f"{clean_username}:{clean_password}"
    auth_header = base64.b64encode(auth_string.encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/json',
        'User-Agent': 'WordPress-Publisher-Bot/1.0'
    }
    endpoint = f"{site_url.rstrip('/')}/wp-json/wp/v2/posts"
    payload = {'title': title, 'content': content, 'status': status}
    
    try:
        print(f"   🚀 Отправка статьи в WordPress...")
        response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
        if response.status_code == 201:
            return response.json()
        print(f"   ❌ Ошибка WordPress: {response.status_code}")
        return None
    except Exception as e:
        print(f"   ❌ Ошибка публикации: {e}")
        return None

def generate_article_template(topic, target_link, anchor_text):
    title = f"{topic}: Insider Secrets & 2026 Strategy Guide"
    img1 = "https://images.unsplash.com/photo-1605870445919-838d190e8e1e?auto=format&fit=crop&w=1200&q=80"
    content = f"""
    <h1>Winning Strategies: {topic}</h1>
    <div class="post-image"><img src="{img1}" alt="Gambling Strategy" style="width:100%; border-radius:8px; margin: 20px 0;"></div>
    
    <h2>The Hidden Algorithm: What Casinos Don't Tell You</h2>
    <p>In the modern gambling world, <strong>{topic}</strong> is driven by complex RNG (Random Number Generators). However, insiders know that patterns often emerge during high-traffic hours.</p>
    <p>Our analysis of over 10,000 rounds suggests that volatility spikes often follow a series of low multipliers (1.0x - 1.2x). This is your signal to enter.</p>
    
    <h3>Insider Insight: The "Blue Streak" Signal</h3>
    <p>Watch for the "Blue Streak" — three consecutive blue outcomes. This is often followed by a Pink (10x+) multiplier. Use this window to place two bets:</p>
    <ul>
        <li><strong>Bet 1:</strong> Cash out at 2.0x to cover costs.</li>
        <li><strong>Bet 2:</strong> Let it ride for the jackpot.</li>
    </ul>

    <h2>Key Aspects to Consider</h2>
    <ul>
        <li>Analyze game patterns using round history tools.</li>
        <li>Manage your bankroll effectively (Stop-loss limits are mandatory).</li>
        <li>Use trusted platforms with fast UPI/Paytm withdrawals.</li>
    </ul>

    <h3>Why Trust Matters?</h3>
    <p>When choosing where to play, always check for licenses. Consider <a href="{target_link}">{anchor_text}</a> as a benchmark for reliability and fair play certifications.</p>
    
    <h2>Pros & Cons</h2>
    <table>
        <tr><th>Pros</th><th>Cons</th></tr>
        <tr><td>High RTP</td><td>High Volatility</td></tr>
        <tr><td>Instant Payouts</td><td>Requires Discipline</td></tr>
    </table>
    
    <p>We recommend starting with small bets to test the waters before diving in.</p>
    """
    return title, content

def update_existing_post(site_url, username, app_password, target_url, anchor, topic):
    print(f"   🔍 Поиск релевантных статей для перелинковки по теме '{topic}'...")
    return None

def generate_article(topic, target_link, anchor_text, author_style='neutral'):
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
        
        # Enhanced Prompt for Indian Niche (English Only) - VERSION 6.0 (Massive Content + Keywords)
        prompt = f"""
        You are an elite iGaming analyst and insider for the Indian market. {STYLE_PROMPTS.get(author_style, STYLE_PROMPTS['neutral'])}
        
        Task: Write a MASSIVE, comprehensive, and high-converting SEO article in HTML format.
        Topic: {topic}
        Main Keyword: {keyword}
        User Intent: {intent} (Users want SECRETS, HACKS, and WINNING TRICKS).
        Target Audience: Indian players (use ₹, mention UPI/Paytm, use specific local context).
        
        # KEYWORDS TO INCLUDE (Mandatory):
        Integrate these keywords naturally throughout the text:
        - "aviator game fake or real"
        - "best aviator game app"
        - "aviator game tricks in hindi" (mention as a common search)
        - "1win aviator login"
        - "aviator predictor apk" (discuss as a myth/scam)
        - "how to withdraw money from aviator"
        - "aviator game signal telegram"
        - "best time to play aviator"
        - "is aviator legal in india"
        - "aviator game cheat code"

        # HTML FORMATTING RULES (STRICT):
        1. **Quick Fact Box**: Immediately BEFORE the first paragraph, insert this EXACT HTML block:
           <div class="quick-fact-box">
             <div class="fact-item"><strong>RTP:</strong> 97%</div>
             <div class="fact-item"><strong>Volatility:</strong> Medium-High</div>
             <div class="fact-item"><strong>Win Rate:</strong> 42%</div>
           </div>

        2. **Main CTA**: After the second paragraph, insert this EXACT shortcode:
           [play_aviator]
           (Strictly use the shortcode, DO NOT wrap it in extra HTML div containers if not necessary, but ensure it is separated from other text).

        3. **Glassmorphism**: Wrap the "Insider Secrets" or "Strategies" section in a <div class="glass-card"> container.
        
        4. Wrap every strategy in a <div class='strategy-card'>.
        5. Use 🎯 emoji for 'Key Aspects'.
        6. Format Pros/Cons using: <div class='grid-pc'><div class='p'><ul><li>Pro 1</li><li>Pro 2</li></ul></div><div class='c'><ul><li>Con 1</li><li>Con 2</li></ul></div></div>.

        Structure Requirements (Critical - MUST FOLLOW):
        1. **Length: EXTREME PRIORITY - Minimum 10,000-12,000 characters (approx 2000-2400 words)**. This is a DEEP DIVE. Every section must be massive.
           - EXPAND every section. Do not list bullet points without explaining them for at least 3-4 paragraphs.
           - Write extremely detailed paragraphs.
        2. **Insight Section**: You MUST include a massive dedicated section titled "Insider Secrets: Algorithm Analysis & 2026 Hacks".
           - Discuss "RNG patterns" and "Server-Seed Logic".
           - Mention specific "Expert Signals" (e.g., "The Double-Pink Martingale Strategy").
           - Make it sound exclusive, expert-level, and highly classified.
        3. Use an engaging <h1> tag.
        4. Use at least 12-16 <h2> subheadings and 8-10 <h3> subheadings within those.
        5. Include a "FAQ" section at the end with 10+ questions (covering legality, withdrawals, hacks).
        6. Use the shortcode [play_aviator] at least 6-8 times in appropriate places.
        7. **CRITICAL**: DO NOT use any direct affiliate links (like 1win.com). Use ONLY the [play_aviator] shortcode for buttons.
        8. For text links, use the anchor "{anchor_text}" and point it to "/go/aviator/?pid=AUTO" (the plugin will handle the ID).
        
        Format Requirement: Return ONLY valid HTML code inside the body. No <html> or <body> tags. No markdown blocks.
        """
    else:
        print(f"Generating content (Style: {author_style}) for topic: {topic}")
        style_instruction = STYLE_PROMPTS.get(author_style, STYLE_PROMPTS['neutral'])
        prompt = f"""
        You are a professional blog writer. {style_instruction}
        Task: Write a comprehensive SEO-optimized article in HTML format.
        Topic: {topic}
        Target Audience: Indian market (use appropriate context).
        
        Requirements:
        1. Length: **Minimum 1000 words**.
        2. Include a natural link to "{target_link}" with anchor text "{anchor_text}".
        3. Use <h2> and <h3> tags for structure.
        4. Include a table or list to break up text.
        5. Use the shortcode [play_aviator] after the second paragraph and at the end.
        6. Return ONLY HTML code. No markdown.
        """
    
    # Raw HTTP Request to bypass library issues
    # gemini-2.0-flash returned 429, meaning it exists!
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={os.getenv('GEMINI_API_KEY')}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    for attempt in range(3):
        try:
            print(f"   🤖 Attempt {attempt+1} calling Gemini...")
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                try:
                    content = result['candidates'][0]['content']['parts'][0]['text']
                    content = content.replace('```html', '').replace('```', '')
                    
                    # INJECT IMAGES LOGIC
                    # Insert random images after first and third paragraphs (or h2)
                    try:
                         parts = content.split('</p>')
                         if len(parts) > 2:
                             img1 = random.choice(GAMBLING_IMAGES)
                             img_html1 = f'<div class="post-image" style="margin: 20px 0;"><img src="{img1}" alt="Gambling illustration" style="width:100%; border-radius:8px;"></div>'
                             parts[1] = parts[1] + img_html1
                         
                         if len(parts) > 5:
                             img2 = random.choice(GAMBLING_IMAGES)
                             img_html2 = f'<div class="post-image" style="margin: 20px 0;"><img src="{img2}" alt="Casino strategy" style="width:100%; border-radius:8px;"></div>'
                             parts[4] = parts[4] + img_html2
                             
                         content = "</p>".join(parts)
                    except Exception as img_err:
                        print(f"⚠️ Image injection failed: {img_err}")

                    return topic, content, "gemini-2.0-flash (Raw HTTP)"
                except (KeyError, IndexError) as e:
                    print(f"⚠️ API Response Parsing Error: {e}. Body: {result}")
                    raise ValueError("Invalid API response structure")
            elif response.status_code == 429:
                print(f"   ⏳ Rate Limited (429). Waiting 60s...")
                time.sleep(60)
                continue
            else:
                print(f"⚠️ API Error {response.status_code}: {response.text}")
                raise ValueError(f"API Error {response.status_code}")
                
        except Exception as e:
            print(f"⚠️ Generation error: {e}.")
            if attempt == 2:
                print("Falling back to template after 3 attempts.")
                t, c = generate_article_template(topic, target_link, anchor_text)
                return t, c, "Template (Fallback)"
            time.sleep(5)
            
    # Fallback if loop finishes without success
    t, c = generate_article_template(topic, target_link, anchor_text)
    return t, c, "Template (Fallback)"

# --- MAIN LOOP ---


def run_tasks(data=None, output_file='results.json'):
    # If no data provided, fetch from sheet
    if not data:
        print("📥 Fetching tasks from Google Sheet...")
        data = fetch_tasks_from_sheet()
        
    if not data:
        print("ℹ️ No pending tasks found in sheet (or JSON).")
        return []
        
    args = sys.argv[1:]
    force_mode = "--force" in args
    
    if force_mode:
        print("🚀 FORCE MODE ACTIVATED: Ignoring schedule dates for the next pending task.")

    results = []
    processed_count = 0
    
    for i, task in enumerate(data):
        print(f"\n--- Task {i+1} ---")
        site_url = task.get('site_url')
        login = task.get('login')
        password = task.get('app_password')
        target_url = task.get('target_links', task.get('target_url')) 
        anchor = task.get('anchor_text', task.get('anchor'))
        topic = task.get('article_topic', task.get('topic'))
        style = task.get('author_style', 'neutral')
        row_id = task.get('row_id') # Row ID for sheet update
        
        # Date Logic
        task_date_str = task.get('date', '').strip()
        
        # If headers are mapped correctly in fetch_tasks_from_sheet, task['date'] should exist
        # But fetch_tasks_from_sheet returns dict with keys: site_url, login, ..., topic.
        # It DOES NOT seem to pass 'date' in the dictionary! 
        # I need to update fetch_tasks_from_sheet to include 'date' first.
        
        if not all([site_url, login, password, target_url, anchor, topic]):
            print(f"Skip task {i+1}: Missing fields.")
            continue

        # Date Filter Logic (One Post Per Day)
        if task_date_str:
            try:
                # Handle potential formats if needed, assuming YYYY-MM-DD
                task_date = datetime.datetime.strptime(task_date_str, "%Y-%m-%d").date()
                today = datetime.date.today()
                
                if task_date > today:
                    if force_mode and processed_count == 0:
                        print(f"🚀 FORCE MODE: Processing future task scheduled for {task_date_str} NOW.")
                    else:
                        print(f"⏳ Task {i+1} scheduled for {task_date_str}. Skipping (future date).")
                        continue
            except ValueError:
                print(f"⚠️ Task {i+1} has invalid date format: {task_date_str}. Processing anyway.")
        
        # Track processed tasks to limit force mode to 1 task if desired (optional)
        # For now, let's allow it to process all "pending" tasks if forced, or just one?
        # User said "run the bot for the next article" (singular).
        if force_mode:
             processed_count += 1
             if processed_count > 1:
                 print("🛑 Force mode limit reached (1 article). Stopping.")
                 break

        # check permissions only for existing post update
        # update_existing_post(site_url, login, password, target_url, anchor, topic)
        
        # Generator now returns model name too
        title, content, model_used = generate_article(topic, target_url, anchor, style)
        
        print(f"Publishing to {site_url}...")
        
        # Dry run logic skipped for brevity, keeping main flow
        post_result = publish_to_wordpress(site_url, login, password, title, content)
        
        status = "success" if post_result else "error"
        link = post_result.get('link') if post_result else None
        
        # UPDATE SHEET IF ROW ID EXISTS
        if row_id:
            update_sheet_status(row_id, status, link if link else "N/A", model_used)
        else:
            # Fallback to old append method if running from CLI JSON
            log_to_google_sheet(site_url, topic, status, link, model_used)

        # Force Google Indexing if link exists
        if status == "success" and link:
            submit_to_google_indexing(link)
        
        task_result = {
            "site": site_url,
            "status": status,
            "new_post_url": link
        }
        results.append(task_result)
        
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    return results

if __name__ == "__main__":
    # If JSON argument provided, use it (Legacy Mode)
    if len(sys.argv) > 1 and sys.argv[1].endswith('.json'):
        try:
            with open(sys.argv[1], 'r') as f:
                user_input = json.load(f)
            run_tasks(user_input)
        except Exception as e:
             print(f"Error reading input file: {e}")
    else:
        # Default mode: Fetch from Sheet
        run_tasks()
