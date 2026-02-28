#!/bin/bash

# ⏰ Setup Cron Job (Daily @ 09:00 AM)
# Usage: bash setup_cron.sh

SERVER_IP="95.217.163.88"

echo "⏰ Configuring Cron on $SERVER_IP..."

ssh root@$SERVER_IP << 'EOF'
    # Define the job
    # Runs at 09:00 every day
    # Triggers the full automation cycle (Publication + Social Promo)
    JOB="0 9 * * * bash /root/pbn_bot/infrastructure/automate_cycle.sh >> /root/pbn_bot/bot.log 2>&1"
    
    # Add to crontab if not exists
    (crontab -l 2>/dev/null | grep -F "$JOB") || (crontab -l 2>/dev/null; echo "$JOB") | crontab -
    
    echo "✅ Cron job added:"
    crontab -l | tail -n 1
EOF
