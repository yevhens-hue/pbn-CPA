import json
from datetime import datetime

def generate_game_schema(game_name="Aviator", rating=4.9, reviews=1254):
    """Generates VideoGame/SoftwareApplication JSON-LD schema."""
    schema = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": game_name,
        "operatingSystem": "ANDROID, IOS, Windows",
        "applicationCategory": "GameApplication",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": str(rating),
            "reviewCount": str(reviews)
        },
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "INR"
        }
    }
    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'

def generate_faq_schema(qa_list):
    """Generates FAQPage JSON-LD schema from a list of (question, answer) tuples."""
    if not qa_list:
        return ""
    
    main_entity = []
    for q, a in qa_list:
        main_entity.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
    
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": main_entity
    }
    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'

def generate_review_schema(item_name, author="Aviator Expert", rating=5):
    """Generates Review JSON-LD schema."""
    schema = {
        "@context": "https://schema.org",
        "@type": "Review",
        "itemReviewed": {
            "@type": "Thing",
            "name": item_name
        },
        "author": {
            "@type": "Person",
            "name": author
        },
        "reviewRating": {
            "@type": "Rating",
            "ratingValue": str(rating),
            "bestRating": "5"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Aviator India Official"
        }
    }
    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'

def get_updated_title(title, lang='en'):
    """Prepend current month/year to titles for 'Freshness' signal."""
    now = datetime.now()
    month_name = now.strftime("%B")
    year = now.year
    
    if lang == 'hi':
        fresh_tag = f"अपडेटेड {month_name} {year}: "
    else:
        fresh_tag = f"Updated {month_name} {year}: "
        
    if fresh_tag.lower() not in title.lower():
        return f"{fresh_tag}{title}"
    return title

def generate_whatsapp_cta(topic):
    """
    Generates a viral-focused WhatsApp share CTA block for the Indian market.
    """
    import urllib.parse
    msg = f"Look at these Aviator tricks I found! 🚀\n\n{topic}\nCheck it here: "
    share_url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
    
    html = f"""
    <!-- WhatsApp Growth CTA -->
    <div class="wa-cta-box" style="background: rgba(37, 211, 102, 0.1); border-left: 4px solid #25D366; padding: 20px; margin: 30px 0; border-radius: 0 12px 12px 0; backdrop-filter: blur(10px); border-top: 1px solid rgba(255,255,255,0.1); border-right: 1px solid rgba(255,255,255,0.1); border-bottom: 1px solid rgba(255,255,255,0.1);">
        <h4 style="margin-top: 0; color: #25D366; font-family: 'Inter', sans-serif;">🔥 Share these signals with your squad!</h4>
        <p style="margin-bottom: 15px; font-family: 'Inter', sans-serif; color: #d1d5db;">Success is better when shared. Send these exclusive tricks to your friends on WhatsApp and win together!</p>
        <a href="{share_url}" target="_blank" rel="nofollow noopener" style="display: inline-flex; align-items: center; gap: 8px; background: #25D366; color: white; padding: 12px 24px; border-radius: 50px; text-decoration: none; font-weight: 700; box-shadow: 0 4px 15px rgba(37, 211, 102, 0.3); font-family: 'Inter', sans-serif; transition: transform 0.2s;">📲 Share on WhatsApp</a>
    </div>
    """
    return html

def get_random_indian_city():
    """Returns a random major Indian city for pSEO targeting."""
    import random
    cities = [
        "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad", 
        "Chennai", "Kolkata", "Surat", "Pune", "Jaipur", 
        "Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", 
        "Bhopal", "Visakhapatnam", "Patna", "Vadodara", "Ghaziabad"
    ]
    return random.choice(cities)
