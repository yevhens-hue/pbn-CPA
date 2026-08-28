#!/bin/bash
# Ежедневный запуск PBN-автоматизации
# Вызывается через cron: 0 10 * * * "/Users/yevhen/Cursor/Тестовое Affilete/daily_task.sh"

echo "---------------------------------------------------"
echo "✅ Batch Started: $(date)"
echo "---------------------------------------------------"

cd "/Users/yevhen/Cursor/Тестовое Affilete/PBN_Automation_Final" || exit 1

python3 agent_manager.py

echo "---------------------------------------------------"
echo "✅ Batch Completed: $(date)"
echo "---------------------------------------------------"
