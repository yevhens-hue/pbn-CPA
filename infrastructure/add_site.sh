#!/bin/bash

# 🚀 Add New Site to PBN
# Usage: bash add_site.sh example.com

DOMAIN=$1
DB_NAME=$(echo $DOMAIN | sed 's/\./_/g')
DB_USER="user_$DB_NAME"
DB_PASS=$(openssl rand -base64 12)

if [ -z "$DOMAIN" ]; then
    echo "Usage: bash add_site.sh domain.com"
    exit 1
fi

echo "🏗 Deploying $DOMAIN..."

# 1. Create Web Directory
mkdir -p /var/www/html/$DOMAIN
cd /var/www/html/$DOMAIN

# 2. Download WordPress
wp core download --allow-root

# 3. Create Database
mysql -u root -pStrongRootPass123! -e "CREATE DATABASE $DB_NAME;"
mysql -u root -pStrongRootPass123! -e "CREATE USER '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';"
mysql -u root -pStrongRootPass123! -e "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';"
mysql -u root -pStrongRootPass123! -e "FLUSH PRIVILEGES;"

# 4. Configure WP
wp core config --dbname=$DB_NAME --dbuser=$DB_USER --dbpass=$DB_PASS --allow-root
wp core install --url=$DOMAIN --title="Best $DOMAIN Site" --admin_user="admin" --admin_password="SuperStrongPassword123" --admin_email="admin@$DOMAIN" --allow-root

# 5. Configure Nginx
cat > /etc/nginx/sites-available/$DOMAIN <<EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    root /var/www/html/$DOMAIN;
    index index.php index.html index.htm;
    location / {
        try_files \$uri \$uri/ /index.php?\$args;
    }
    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock; # Adjust PHP version if needed
    }
}
EOF

ln -s /etc/nginx/sites-available/$DOMAIN /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

# 6. SSL (Let's Encrypt)
# Uncomment next line to auto-enable HTTPS (requires domain to point to server IP)
# certbot --nginx -d $DOMAIN --non-interactive --agree-tos -m admin@$DOMAIN

# 7. Setup Application Password for our Robot
# wp user application-password create admin "PBN_Robot" --allow-root

# 8. Set Permissions
chown -R www-data:www-data /var/www/html/$DOMAIN

echo "🎉 Site $DOMAIN created!"
echo "WP Admin: http://$DOMAIN/wp-admin"
echo "User: admin"
echo "Pass: SuperStrongPassword123"
echo "DB Pass: $DB_PASS"
