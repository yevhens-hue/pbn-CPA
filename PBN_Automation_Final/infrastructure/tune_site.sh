#!/bin/bash
# 🛠 Tune WP Site — Enhanced SEO Setup
# Usage: bash tune_site.sh domain.com
# Run on the server where WordPress is installed

DOMAIN=$1
if [ -z "$DOMAIN" ]; then
    echo "❌ Usage: bash tune_site.sh domain.com"
    exit 1
fi

WEB_DIR="/var/www/html/$DOMAIN"
WP_CLI="wp --path=$WEB_DIR --allow-root"
HTACCESS="$WEB_DIR/.htaccess"

echo "🎨 Tuning $DOMAIN for SEO..."

# ---- 1. Theme ----
echo "[1/6] Installing GeneratePress (fast, lightweight)..."
$WP_CLI theme install generatepress --activate
$WP_CLI theme delete twentytwentyfour twentytwentythree twentytwentytwo 2>/dev/null

# ---- 2. SEO Plugin ----
echo "[2/6] Installing Yoast SEO..."
$WP_CLI plugin install wordpress-seo --activate
# Configure basic Yoast SEO options
$WP_CLI option update wpseo '{"enable_xml_sitemap":true}' --format=json

# ---- 3. Caching Plugin ----
echo "[3/6] Installing WP Super Cache..."
$WP_CLI plugin install wp-super-cache --activate
$WP_CLI plugin activate wp-super-cache

# ---- 4. Clean Garbage ----
echo "[4/6] Cleaning default content..."
$WP_CLI post delete 1 --force 2>/dev/null  # Hello World
$WP_CLI post delete 2 --force 2>/dev/null  # Sample Page
$WP_CLI plugin delete hello akismet 2>/dev/null

# ---- 5. Permalinks (Critical for SEO) ----
echo "[5/6] Setting Permalinks to /%postname%/..."
$WP_CLI rewrite structure '/%postname%/'
$WP_CLI rewrite flush

# ---- 6. .htaccess — gzip + Browser Caching ----
echo "[6/6] Adding gzip + browser cache headers to .htaccess..."

cat >> "$HTACCESS" << 'HTACCESS_RULES'

# ========= SEO Performance (Auto-Added by tune_site.sh) =========

# Enable GZIP Compression
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/plain text/html text/xml text/css
  AddOutputFilterByType DEFLATE application/javascript application/x-javascript
  AddOutputFilterByType DEFLATE application/json application/ld+json
  AddOutputFilterByType DEFLATE image/svg+xml
</IfModule>

# Browser Caching
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/jpg  "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/png  "access plus 1 year"
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 month"
  ExpiresByType text/css   "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
  ExpiresByType text/html  "access plus 1 hour"
</IfModule>

# Security Headers (also help SEO trust)
<IfModule mod_headers.c>
  Header set X-Content-Type-Options "nosniff"
  Header set X-Frame-Options "SAMEORIGIN"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>

# Force HTTPS
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteCond %{HTTPS} off
  RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
</IfModule>

HTACCESS_RULES

echo ""
echo "✅ Done! $DOMAIN is now SEO-tuned:"
echo "   ✔ GeneratePress theme"
echo "   ✔ Yoast SEO + Sitemap"
echo "   ✔ WP Super Cache"
echo "   ✔ /%postname%/ permalinks"
echo "   ✔ gzip + browser caching in .htaccess"
echo "   ✔ HTTPS redirect"
echo ""
echo "📋 Next steps:"
echo "   1. Upload functions.php changes to your active theme"
echo "   2. Run: python3 seo_audit.py https://$DOMAIN/"
echo "   3. Submit sitemap: https://$DOMAIN/sitemap_index.xml to Google Search Console"
