#!/bin/bash

# ==========================================
# 🚀 PBN Automation Daily Runner
# ==========================================
# Add this script to crontab to run daily:
# 0 10 * * * /path/to/daily_task.sh >> /path/to/cron.log 2>&1

# 1. Set Project Directory (Change this on VPS!)
cd "$(dirname "$0")"

# 2. Activate Virtual Environment (if used)
# source venv/bin/activate

# 3. Random Delay (Safety Feature)
# Waits between 1 and 60 minutes to simulate human behavior start time
DELAY=$((RANDOM % 3600))
echo "🕒 Waiting for $(($DELAY / 60)) minutes before starting..."
sleep $DELAY

# 4. Run Publication Cycle
echo "🚀 Starting PBN Publication Batch: $(date)"
python3 publish_post.py sites_data.json

# 5. Run Analytics & Sync to DB
echo "📊 Updating Dashboard & Database..."
python3 dashboard.py

# 6. Optional: Health Check / Cleanup
echo "✅ Batch Completed: $(date)"
echo "---------------------------------------------------"
