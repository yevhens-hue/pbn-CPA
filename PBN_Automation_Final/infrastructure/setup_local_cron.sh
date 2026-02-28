#!/bin/bash

# ⏰ Setup Local Cron Job (Daily @ 09:00 AM)
# This script adds the automation cycle to your macOS crontab.

# 1. Paths
SCRIPT_PATH="/Users/yevhen/Cursor/Тестовое Affilete/PBN_Automation_Final/infrastructure/automate_cycle.sh"
AUDIT_PATH="/Users/yevhen/Cursor/Тестовое Affilete/PBN_Automation_Final/seo_audit.py"

if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ Error: Publication script not found at $SCRIPT_PATH"
    exit 1
fi

# 2. Define Jobs
# Publication: Runs at 09:00 every day
JOB_PUB="0 9 * * * bash \"$SCRIPT_PATH\" >> \"/Users/yevhen/Cursor/Тестовое Affilete/PBN_Automation_Final/logs/cron.log\" 2>&1"
# Audit: Runs at 10:00 every Monday
JOB_AUDIT="0 10 * * 1 python3 \"$AUDIT_PATH\" >> \"/Users/yevhen/Cursor/Тестовое Affilete/PBN_Automation_Final/logs/seo_audit.log\" 2>&1"

# 3. Add to crontab if they don't already exist
(crontab -l 2>/dev/null | grep -F "$SCRIPT_PATH") || (crontab -l 2>/dev/null; echo "$JOB_PUB") | crontab -
(crontab -l 2>/dev/null | grep -F "$AUDIT_PATH") || (crontab -l 2>/dev/null; echo "$JOB_AUDIT") | crontab -

echo "✅ Local cron jobs have been configured:"
crontab -l | grep -E "automate_cycle.sh|seo_audit.py"

echo "📝 Publication logs: /Users/yevhen/Cursor/Тестовое Affilete/PBN_Automation_Final/logs/cron.log"
echo "📝 SEO Audit logs: /Users/yevhen/Cursor/Тестовое Affilete/PBN_Automation_Final/logs/seo_audit.log"
