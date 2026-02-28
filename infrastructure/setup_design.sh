#!/bin/bash

# ==========================================
# AVIATOR DESIGN SETUP SCRIPT
# Installs GeneratePress, Configures Menus, Injects CSS
# Usage: bash infrastructure/setup_design.sh
# ==========================================

# Configuration
DOMAIN=$1
WP_PATH=$2 # Allow manual path override

if [ -z "$WP_PATH" ]; then
    WP_PATH="/var/www/html"

    # Auto-detect WP Path if default fails
    if [ ! -f "$WP_PATH/wp-config.php" ]; then
        echo "⚠️ WordPress not found at $WP_PATH. Searching..."
        # Check domain folder first
        if [ ! -z "$DOMAIN" ] && [ -d "/var/www/$DOMAIN" ]; then
            WP_PATH="/var/www/$DOMAIN"
        else
            # Find any folder in /var/www/ with wp-config.php
            FOUND_PATH=$(find /var/www -maxdepth 2 -name "wp-config.php" | head -n 1)
            if [ ! -z "$FOUND_PATH" ]; then
                WP_PATH=$(dirname "$FOUND_PATH")
                echo "✅ Found WordPress at: $WP_PATH"
            else
                echo "❌ CRITICAL: Could not find WordPress installation!"
                echo "💡 Try running: bash setup_design.sh domain.com /absolute/path/to/wordpress"
                exit 1
            fi
        fi
    fi
fi

THEME_SLUG="generatepress"
# Use absolute path to ensure file is found regardless of CWD
CSS_FILE="/root/pbn_bot/data/aviator_theme.css"


echo "🎨 Starting Aviator Design Setup for $WP_PATH..."

# 1. Install & Activate Theme
echo "📦 Installing theme: $THEME_SLUG..."
wp theme install $THEME_SLUG --activate --path=$WP_PATH --allow-root

# 1.1 Set Site Title & Tagline
echo "🏷️ Setting Site Title..."
wp option update blogname "Aviator India Official" --path=$WP_PATH --allow-root
wp option update blogdescription "Winning Strategies & App Download 2026" --path=$WP_PATH --allow-root

# 1.2 Set Permalinks (SEO)
echo "🔗 Setting Permalinks..."
wp rewrite structure '/%postname%/' --hard --path=$WP_PATH --allow-root


# 2. Add Custom CSS (Aviator Dark Mode)
if [ -f "$CSS_FILE" ]; then
    echo "💅 Injecting Custom CSS from $CSS_FILE..."
    CSS_CONTENT=$(cat $CSS_FILE)
    
    # Method: Create a 'custom_css' post (Standard WP way)
    # Check if a custom css post already exists for this theme
    EXISTING_CSS_ID=$(wp post list --post_type=custom_css --post_title="$THEME_SLUG" --format=ids --path=$WP_PATH --allow-root)
    
    if [ -z "$EXISTING_CSS_ID" ]; then
        echo "   Creating new CSS post..."
        wp post create --post_type=custom_css --post_title="$THEME_SLUG" --post_content="$CSS_CONTENT" --post_status=publish --path=$WP_PATH --allow-root
    else
        echo "   Updating existing CSS post (ID: $EXISTING_CSS_ID)..."
        wp post update $EXISTING_CSS_ID --post_content="$CSS_CONTENT" --path=$WP_PATH --allow-root
    fi
    
    # Also set as theme mod just in case (some themes use this)
    wp theme mod set custom_css_post_id $EXISTING_CSS_ID --path=$WP_PATH --allow-root
else
    echo "⚠️ CSS file not found at $CSS_FILE! Skipping CSS injection."
fi

# 3. Configure Navigation Menu
MENU_NAME="Main Aviator Menu"
echo "ww Configuring Navigation: $MENU_NAME..."

# Check if menu exists
MENU_EXISTS=$(wp menu list --format=json --path=$WP_PATH --allow-root | grep "$MENU_NAME")

if [ -z "$MENU_EXISTS" ]; then
    wp menu create "$MENU_NAME" --path=$WP_PATH --allow-root
    
    # Add items
    wp menu item add-custom "$MENU_NAME" "Aviator Game" "/" --path=$WP_PATH --allow-root
    wp menu item add-custom "$MENU_NAME" "Download App" "/download-app/" --classes="download-btn" --path=$WP_PATH --allow-root
    wp menu item add-custom "$MENU_NAME" "Strategies" "/strategies/" --path=$WP_PATH --allow-root
    wp menu item add-custom "$MENU_NAME" "Bonuses" "/bonuses/" --path=$WP_PATH --allow-root
    
    # Assign to primary location
    wp menu location assign "$MENU_NAME" primary --path=$WP_PATH --allow-root
    echo "✅ Menu created and assigned."
else
    echo "ℹ️ Menu '$MENU_NAME' already exists. Skipping."
fi

# 4. Create "Download App" Page (Landing Page Placeholder)
echo "📄 Creating 'Download App' page..."
PAGE_EXISTS=$(wp post list --post_type=page --name="download-app" --format=ids --path=$WP_PATH --allow-root)

if [ -z "$PAGE_EXISTS" ]; then
    wp post create --post_type=page --post_title="Download Aviator App" --post_name="download-app" --post_status=publish --post_content="<!-- wp:heading --><h1>Download Aviator APK for Android & iOS</h1><!-- /wp:heading --><!-- wp:paragraph --><p>Get the official Aviator game app with exclusive bonuses.</p><!-- /wp:paragraph --><!-- wp:html --><a href='#' class='aviator-cta-btn'>🚀 Download App Now</a><!-- /wp:html -->" --path=$WP_PATH --allow-root
else
    echo "ℹ️ Page 'Download App' already exists."
fi

echo "✅ Design Setup Complete! Visit the site to see the Dark Theme."
echo "🧹 Flushing Cache..."
wp cache flush --path=$WP_PATH --allow-root

