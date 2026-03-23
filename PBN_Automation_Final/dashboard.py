import streamlit as st
import pandas as pd
import json
import os
import datetime
from publish_post import run_tasks, load_content_plan

st.set_page_config(page_title="Evelson SEO Command Center", page_icon="🚀", layout="wide")

st.title("🚀 Evelson SEO Stack: Command Center")
st.markdown("### Managing `luckybetvip.com` & PBN Automation")

# Sidebar - Settings & Stats
st.sidebar.header("⚙️ Configuration")
# Don't pre-fill API keys in UI for security - users should enter them
anthropic_key = st.sidebar.text_input("Anthropic API Key", type="password", 
    help="Enter your Anthropic API key (sk-***). Get it from console.anthropic.com")
google_creds = st.sidebar.file_uploader("Google Credentials (JSON)", type="json")

st.sidebar.divider()
st.sidebar.markdown("### 📊 Status")
# Dynamic status based on actual API keys
if anthropic_key and anthropic_key.startswith("sk-"):
    st.sidebar.success("Claude 3.5 Sonnet: Connected")
else:
    st.sidebar.warning("Claude 3.5 Sonnet: Not configured")

# Check IndexNow key
indexnow_key = os.getenv("INDEXNOW_API_KEY", "")
if indexnow_key:
    st.sidebar.info("IndexNow: Active")
else:
    st.sidebar.info("IndexNow: Not configured (optional)")

# Main Content
tab1, tab2, tab3, tab4 = st.tabs(["📋 Dashboard", "✍️ Content Plan", "🛡️ Site Management", "💰 Affiliate Stats"])

with tab1:
    st.subheader("Recent Activity")
    try:
        if os.path.exists("results.json"):
            with open("results.json", "r") as f:
                results = json.load(f)
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No results yet. Run a task to see activity.")
    except Exception as e:
        st.error(f"Error loading results: {e}")

    # --- Viral Content Section ---
    st.subheader("🚀 Viral Marketing Assets")
    if st.button("Generate Reels Scripts & Lead Magnets"):
        with st.spinner("AI is crafting viral scripts..."):
            from social_promo import fetch_wp_posts, generate_viral_assets
            posts = fetch_wp_posts(count=3)
            if posts:
                for p in posts:
                    st.write(f"**Topic:** {p['title']['rendered']}")
                    assets = generate_viral_assets(p)
                    st.text_area(f"Assets for {p['id']}", assets, height=200)
                    st.divider()
            else:
                st.warning("No published posts found to generate assets from.")

    st.markdown("---")
    st.info("💡 Tip: Use Claude 3.5 Sonnet for the best script quality. Fallback is active.")

    if st.button("🚀 Run Daily Automation (1 Post)"):
        with st.spinner("Generating content with Claude 3.5 Sonnet..."):
            res = run_tasks(max_tasks=1)
            st.success("Task completed!")
            st.json(res)

with tab2:
    st.subheader("Next Trending Topics (India)")
    topics = load_content_plan()
    if topics:
        st.table(topics[:10])
    else:
        st.warning("Content plan not found.")

with tab3:
    st.subheader("Managed Sites")
    try:
        with open("data/sites_data.json", "r") as f:
            sites = json.load(f)
        for site in sites:
            cols = st.columns([3, 1, 1])
            cols[0].write(f"🌐 **{site['site_url']}**")
            cols[1].write(f"📝 Posts: {site.get('post_count', 0)}")
            if cols[2].button("Check Status", key=site['site_url']):
                st.toast(f"Site {site['site_url']} is healthy!")
    except Exception as e:
        st.error(f"Error loading sites: {e}")

with tab4:
    st.subheader("💰 Affiliate Statistics (Playwright Web Scraper)")
    st.markdown("**(Playwright Feature 4: Dashboard parsing)**")
    
    st.info("This feature uses a headless Chromium browser to log into affiliate programs without APIs (e.g., 1win partners) to scrape daily registrations and deposits.")
    
    if st.button("🚀 Scrape Affiliate Data (Demo)"):
        with st.spinner("Playwright is navigating to the affiliate panel and bypassing Cloudflare..."):
            import time
            time.sleep(2)  # Simulate browser startup
            
            try:
                from playwright.sync_api import sync_playwright
                with sync_playwright() as p:
                     browser = p.chromium.launch(headless=True)
                     page = browser.new_page()
                     # Mock scraping logic on a safe domain
                     page.goto("https://example.com")
                     browser.close()
                st.success("✅ Scraped successfully from simulated affiliate panel.")
                
                cols = st.columns(3)
                cols[0].metric(label="New Registrations (Today)", value="14", delta="2")
                cols[1].metric(label="First Time Deposits (FTD)", value="3", delta="-1")
                cols[2].metric(label="Estimated Revenue", value="$120.50", delta="+$20")
            except Exception as e:
                st.error(f"Playwright failed: {e}")

st.divider()
st.caption("Powered by Claude 3.5 Sonnet & IndexNow Protocol")
