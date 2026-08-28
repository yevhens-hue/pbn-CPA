import json

new_topics = [
    {
        "category": "Crash Games",
        "keyword": "aviator autoplay hack",
        "title": "Aviator Autoplay Hack 2026: Fact or Fiction?",
        "intent": "analysis"
    },
    {
        "category": "Crash Games",
        "keyword": "plinko game strategy",
        "title": "Plinko Game Strategy: Dropping the Ball for Max Wins",
        "intent": "strategy"
    },
    {
        "category": "Crash Games",
        "keyword": "minesweeper casino mathematics",
        "title": "The Mathematics Behind Mines Casino Games: Avoiding the Bombs",
        "intent": "guide"
    },
    {
        "category": "General",
        "keyword": "high roller casinos india",
        "title": "Best High-Roller Casinos in India: VIP Limits and Perks",
        "intent": "list"
    },
    {
        "category": "Payments",
        "keyword": "ethereum vs bitcoin gambling",
        "title": "Ethereum vs Bitcoin Gambling in India: Pros and Cons",
        "intent": "comparison"
    },
    {
        "category": "Local Games",
        "keyword": "indian rummy variations",
        "title": "Indian Rummy Variations: Learn Points, Pool, and Deals Rummy",
        "intent": "guide"
    },
    {
        "category": "Crash Games",
        "keyword": "aviator whatsapp signals",
        "title": "Aviator Signals on WhatsApp: Trustworthy Advice or Complete Scam?",
        "intent": "review"
    },
    {
        "category": "Live Casino",
        "keyword": "baccarat trends",
        "title": "How to Read Baccarat Trends Like a Professional Player",
        "intent": "strategy"
    }
]

with open('data/content_plan_india.json', 'r') as f:
    data = json.load(f)

data['topics'].extend(new_topics)

with open('data/content_plan_india.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Topics added!")
