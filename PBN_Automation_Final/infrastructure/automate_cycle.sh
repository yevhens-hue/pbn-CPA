#!/bin/bash
# PBN Automation Cycle — LuckyBetVIP
# =================================
# Orchestrates publishing and social promotion.

# 1. Config
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$BASE_DIR/logs/daily_cycle.log"
PYTHON_CMD="$BASE_DIR/venv/bin/python3"

# Fallback to system python if venv doesn't exist (local testing)
if [ ! -f "$PYTHON_CMD" ]; then
    PYTHON_CMD="python3"
fi

# Ensure we are in the correct directory
cd "$BASE_DIR" || exit

echo "--- STARTING PBN CYCLE: $(date) ---" >> "$LOG_FILE"

# 2. Logic: strictly ONE article per day, alternating languages
DAY_OF_YEAR=$(date +%j)
if [ $((DAY_OF_YEAR % 2)) -eq 0 ]; then
    echo "🚀 [$(date)] Cycle: English Article (Even Day Target)..." >> "$LOG_FILE"
    $PYTHON_CMD publish_post.py --limit 1 >> "$LOG_FILE" 2>&1
else
    echo "🚀 [$(date)] Cycle: Hindi Article (Odd Day Target)..." >> "$LOG_FILE"
    $PYTHON_CMD publish_post.py --hindi --limit 1 >> "$LOG_FILE" 2>&1
fi

# 3. Social Promotion (Latest articles)
echo "📣 [$(date)] Promoting latest articles on Socials (Telegram, Telegra.ph, Reddit)..." >> "$LOG_FILE"
$PYTHON_CMD social_promo.py --telegram --telegraph --reddit >> "$LOG_FILE" 2>&1

echo "--- CYCLE COMPLETED: $(date) ---" >> "$LOG_FILE"
echo "---------------------------------" >> "$LOG_FILE"

exit 0
