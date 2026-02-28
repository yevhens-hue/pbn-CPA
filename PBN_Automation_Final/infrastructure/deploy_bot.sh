#!/bin/bash

# 🚀 Deploy Bot to Server
# Usage: bash deploy_bot.sh

SERVER_IP="95.217.163.88"
REMOTE_DIR="/root/pbn_bot"

# Navigate to the root of the bot directory (one level up from infrastructure/)
cd "$(dirname "$0")/.." || exit

echo "📦 Packaging bot..."
# Remove old zip
rm -f bot_package.zip

# Zip necessary files
zip -r bot_package.zip core/ data/ infrastructure/ .env requirements.txt *.py *.php scraper-483621-3ae386cecfc1.json pbn-high-roller-plugin/

echo "📤 Uploading to $SERVER_IP..."
scp bot_package.zip root@$SERVER_IP:$REMOTE_DIR.zip

echo "🏗 Installing on server..."
ssh root@$SERVER_IP << 'EOF'
    # 1. Prepare Directory
    mkdir -p /root/pbn_bot
    unzip -o /root/pbn_bot.zip -d /root/pbn_bot
    rm /root/pbn_bot.zip
    
    # 2. Setup Venv
    cd /root/pbn_bot
    apt update && apt install -y python3-venv python3-pip
    python3 -m venv venv
    
    # 3. Install Requirements
    source venv/bin/activate
    pip install -r requirements.txt
    
    echo "✅ Bot deployed successfully!"
EOF

rm bot_package.zip
