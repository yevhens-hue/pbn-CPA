#!/usr/bin/env python3
"""
auto_commenter.py — Генерирует и публикует 1-2 реалистичных комментария
на каждую новую статью WordPress через REST API.

Защита от обнаружения:
- Уникальные индийские персонажи с разными именами, email, стилем
- Groq генерирует контекстный комментарий по ТЕМЕ статьи (не шаблон)
- Рандомная задержка 15–90 минут после публикации статьи
- Разная длина и стиль (вопрос, восхищение, личный опыт)
- Автоматическое одобрение через app_password (комментарий сразу виден)
"""

import os
import json
import random
import time
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# ──────────────────────────────────────────────
# Банк персонажей (индийская аудитория)
# ──────────────────────────────────────────────
PERSONAS = [
    {"name": "Rahul Sharma",    "email": "rahul.sharma92@gmail.com",   "style": "curious"},
    {"name": "Priya Nair",      "email": "priya.nair.in@yahoo.co.in",  "style": "enthusiastic"},
    {"name": "Amit Verma",      "email": "amitverma88@rediffmail.com",  "style": "experienced"},
    {"name": "Sunita Patel",    "email": "sunita_patel@hotmail.com",   "style": "skeptical"},
    {"name": "Vikram Singh",    "email": "viksingh777@gmail.com",      "style": "experienced"},
    {"name": "Deepa Krishnan",  "email": "deepakrishnan@outlook.com",  "style": "curious"},
    {"name": "Ravi Kumar",      "email": "ravi.kumar.bet@gmail.com",   "style": "enthusiastic"},
    {"name": "Ananya Das",      "email": "ananya.das99@gmail.com",     "style": "skeptical"},
    {"name": "Manish Gupta",    "email": "manish.g.india@gmail.com",   "style": "experienced"},
    {"name": "Pooja Mehta",     "email": "pooja.mehta.play@yahoo.in",  "style": "curious"},
    {"name": "Arjun Choudhury", "email": "arjun.choudhury.kol@gmail.com", "style": "enthusiastic"},
    {"name": "Sonal Jain",      "email": "sonal.jain.ca@gmail.com",    "style": "skeptical"},
    {"name": "Karan Bajaj",     "email": "karan.bajaj.official@gmail.com", "style": "high-roller"},
    {"name": "Neha Kapoor",     "email": "nehakapoor.vlog@gmail.com",  "style": "high-roller"},
    {"name": "Sameer Deshmukh", "email": "s.deshmukh85@gmail.com",     "style": "experienced"},
]

STYLE_PROMPTS = {
    "curious": "Write as someone curious who is new to this topic. Ask 1-2 specific questions about the details in the article. Keep it short (2-3 sentences).",
    "enthusiastic": "Write as someone excited who just tried this and had good results. Share brief enthusiasm and one specific tip. Keep it natural (2-3 sentences).",
    "experienced": "Write as a seasoned player sharing additional context from your own experience that relates to this article. Add one piece of practical advice (2-4 sentences).",
    "skeptical": "Write as someone mildly skeptical but genuinely curious. Ask for clarification about one specific claim in the article. Be polite (2-3 sentences).",
    "high-roller": "Write as a high-stakes player who only cares about big wins and risk management. Use Hinglish and aggressive slang. (3-4 sentences).",
    "doubter": "Write as someone who is unsure if this works but is willing to try. Ask for a proof or a specific multiplier. Use Hinglish. (2-3 sentences).",
}


def generate_comment(post_title: str, topic: str, persona: dict) -> Optional[str]:
    """
    Генерирует реалистичный комментарий через Groq API.
    """
    groq_key = os.getenv("GROQ_API_KEY", "").strip()
    if not groq_key:
        print("⚠️ GROQ_API_KEY not set. Cannot generate comment.")
        return None

    style_instruction = STYLE_PROMPTS.get(persona["style"], STYLE_PROMPTS["curious"])
    prompt = f"""You are commenting on a blog post titled: "{post_title}" (topic: {topic}).
    
{style_instruction}

Important rules:
- Write ONLY the comment text, no intro, no quotes, no markdown
- Sound like a real Indian online gambler or bettor
- Use Hinglish (mix of Hindi in English script and English) where natural (e.g., 'Bhai', 'Yaar', 'Mota win', 'Paisa').
- Reference something specific from the title naturally
- Do NOT use phrases like "Great article!", "Nice post!", "Thanks for sharing!"
- Mix in natural grammar imperfections (occasional missing comma, informal phrasing)
- Write in a natural, street-smart Indian style.
"""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {groq_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You write realistic blog comments for iGaming content."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 200,
        "temperature": 0.9,  # Высокая температура = больше вариативности
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            text = resp.json()["choices"][0]["message"]["content"].strip()
            # Убираем кавычки если Groq обернул в них
            if text.startswith('"') and text.endswith('"'):
                text = text[1:-1]
            return text
        else:
            print(f"❌ Groq error {resp.status_code}: {resp.text[:200]}")
            return None
    except Exception as e:
        print(f"❌ Groq request failed: {e}")
        return None


def post_comment_to_wordpress(
    site_url: str,
    login: str,
    app_password: str,
    post_id: int,
    author_name: str,
    author_email: str,
    comment_text: str,
) -> bool:
    """
    Публикует комментарий напрямую через WP REST API.
    Использует Application Password администратора для автоматического одобрения.
    """
    api_url = f"{site_url.rstrip('/')}/wp-json/wp/v2/comments"
    
    payload = {
        "post": post_id,
        "author_name": author_name,
        "author_email": author_email,
        "content": comment_text,
        "status": "approved",  # Сразу одобряем (требует прав администратора)
    }

    try:
        resp = requests.post(
            api_url,
            json=payload,
            auth=(login, app_password),
            timeout=20
        )
        if resp.status_code in (200, 201):
            comment_id = resp.json().get("id", "?")
            print(f"   ✅ Comment #{comment_id} posted by '{author_name}'")
            return True
        else:
            print(f"   ❌ WP API error {resp.status_code}: {resp.text[:200]}")
            return False
    except Exception as e:
        print(f"   ❌ Request failed: {e}")
        return False


def get_post_id_from_url(site_url: str, login: str, app_password: str, post_url: str) -> Optional[int]:
    """
    Определяет WordPress Post ID по URL статьи.
    """
    # Попытка через WP REST API search
    slug = post_url.rstrip("/").split("/")[-1]
    api_url = f"{site_url.rstrip('/')}/wp-json/wp/v2/posts"
    
    try:
        resp = requests.get(
            api_url,
            params={"slug": slug, "per_page": 1},
            auth=(login, app_password),
            timeout=15
        )
        if resp.status_code == 200:
            posts = resp.json()
            if posts:
                return posts[0]["id"]
        print(f"   ⚠️ Could not find post ID for slug: {slug}")
        return None
    except Exception as e:
        print(f"   ❌ Error fetching post ID: {e}")
        return None


def comment_on_post(
    site_url: str,
    login: str,
    app_password: str,
    post_url: str,
    post_title: str,
    topic: str,
    num_comments: int = 2,
    delay_minutes: int = 0,
):
    """
    Основная функция: генерирует и публикует комментарии для одной статьи.
    delay_minutes=0 означает немедленную публикацию (для catch-up).
    """
    if delay_minutes > 0:
        delay_secs = delay_minutes * 60
        print(f"⏳ Waiting {delay_minutes} min before commenting on: {post_title}")
        time.sleep(delay_secs)

    print(f"\n💬 Posting {num_comments} comment(s) on: {post_title}")
    print(f"   URL: {post_url}")

    # Получаем WordPress ID статьи
    post_id = get_post_id_from_url(site_url, login, app_password, post_url)
    if not post_id:
        print("   ⚠️ Skipping comments — post ID not found.")
        return

    # Выбираем уникальных персонажей
    chosen_personas = random.sample(PERSONAS, min(num_comments, len(PERSONAS)))

    for i, persona in enumerate(chosen_personas):
        comment_text = generate_comment(post_title, topic, persona)
        if not comment_text:
            print(f"   ⚠️ Could not generate comment for persona: {persona['name']}")
            continue

        print(f"   → [{persona['style'].upper()}] {persona['name']}: {comment_text[:80]}...")
        
        success = post_comment_to_wordpress(
            site_url, login, app_password,
            post_id, persona["name"], persona["email"], comment_text
        )

        # Задержка между комментариями (15-60 секунд), чтобы не выглядело как спам
        if i < len(chosen_personas) - 1:
            gap = random.randint(15, 60)
            print(f"   ⏱ Waiting {gap}s before next comment...")
            time.sleep(gap)


def comment_on_recent_posts(
    site_url: str,
    login: str,
    app_password: str,
    num_to_comment: int = 5,
    comments_per_post: int = 2,
):
    """
    Находит последние статьи БЕЗ комментариев и оставляет comment_per_post.
    Полезно для начального прогона на всех старых статьях.
    """
    api_url = f"{site_url.rstrip('/')}/wp-json/wp/v2/posts"
    
    try:
        resp = requests.get(
            api_url,
            params={"per_page": 50, "orderby": "date", "order": "desc", "comment_count": 0},
            auth=(login, app_password),
            timeout=20
        )
        if resp.status_code != 200:
            print(f"❌ Could not fetch posts: {resp.status_code}")
            return
        
        posts = resp.json()
        processed = 0
        for post in posts:
            if processed >= num_to_comment:
                break
                
            title = post.get("title", {}).get("rendered", "Unknown")
            url = post.get("link", "")
            post_id = post.get("id")
            
            # Check if post has comments by calling the replies endpoint
            # Rate limiting: small delay to avoid overwhelming the server
            time.sleep(random.uniform(1, 3))
            replies_url = f"{site_url.rstrip('/')}/wp-json/wp/v2/comments"
            r_comments = requests.get(replies_url, params={"post": post_id, "per_page": 1}, auth=(login, app_password))
            count = int(r_comments.headers.get("X-WP-Total", 0))
            
            if count > 0:
                print(f"⏭️ Skipping '{title}' (already has {count} comments)")
                continue

            print(f"\n💬 Target: {title}")
            processed += 1
            
            chosen_personas = random.sample(PERSONAS, min(comments_per_post, len(PERSONAS)))
            for i, persona in enumerate(chosen_personas):
                comment_text = generate_comment(title, title, persona)
                if not comment_text:
                    continue
                    
                print(f"   → [{persona['style'].upper()}] {persona['name']}: {comment_text[:80]}...")
                post_comment_to_wordpress(
                    site_url, login, app_password,
                    post_id, persona["name"], persona["email"], comment_text
                )
                
                if i < len(chosen_personas) - 1:
                    time.sleep(random.randint(15, 45))

            # Задержка между статьями
            gap = random.randint(30, 90)
            print(f"⏱ Waiting {gap}s before next post...")
            time.sleep(gap)

    except Exception as e:
        print(f"❌ Error in comment_on_recent_posts: {e}")


# ──────────────────────────────────────────────
# Запуск из командной строки
# ──────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    SITE_URL      = "https://luckybetvip.com"
    LOGIN         = "admin"
    APP_PASSWORD  = os.getenv("WP_APP_PASSWORD", "4SvP8Q4hqfxnsDo6xS351Xcr")

    # Режим 1: python auto_commenter.py --backfill
    # Оставляет комментарии на последние 10 статей без комментариев
    if "--backfill" in sys.argv:
        count = 10
        if "--count" in sys.argv:
            try:
                count = int(sys.argv[sys.argv.index("--count") + 1])
            except (IndexError, ValueError):
                pass
        print(f"🔄 Backfill mode: commenting on {count} old posts...")
        comment_on_recent_posts(SITE_URL, LOGIN, APP_PASSWORD, num_to_comment=count)

    # Режим 2: python auto_commenter.py --url <post_url> --title "..." --topic "..."
    elif "--url" in sys.argv:
        try:
            url_idx    = sys.argv.index("--url")
            title_idx  = sys.argv.index("--title")
            topic_idx  = sys.argv.index("--topic")

            post_url   = sys.argv[url_idx + 1]
            post_title = sys.argv[title_idx + 1]
            post_topic = sys.argv[topic_idx + 1]
            
            delay = 0
            if "--delay" in sys.argv:
                delay_idx = sys.argv.index("--delay")
                delay = int(sys.argv[delay_idx + 1])

            comment_on_post(
                SITE_URL, LOGIN, APP_PASSWORD,
                post_url, post_title, post_topic,
                num_comments=2,
                delay_minutes=delay,
            )
        except (IndexError, ValueError) as e:
            print(f"❌ Invalid arguments: {e}")
            print("Usage: python auto_commenter.py --url <url> --title '<title>' --topic '<topic>' [--delay <minutes>]")
    else:
        print("Auto Commenter")
        print("Usage:")
        print("  python auto_commenter.py --backfill [--count N]")
        print("  python auto_commenter.py --url <url> --title '<title>' --topic '<topic>' [--delay N]")
