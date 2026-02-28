#!/bin/bash

# 🚀 PBN Server Auto-Setup (Ubuntu 22.04/24.04)
# Run this on your FRESH VPS as root:
# curl -O https://raw.githubusercontent.com/.../setup_server.sh && bash setup_server.sh

# 1. Update OS
apt update && apt upgrade -y

# 2. Install Nginx, MariaDB, PHP, Unzip, Certbot
apt install -y nginx mariadb-server php-fpm php-mysql php-curl php-gd php-mbstring php-xml php-zip unzip certbot python3-certbot-nginx

# 3. Secure MySQL
# (Automated secure installation)
mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED VIA mysql_native_password;"
mysql -e "SET PASSWORD FOR 'root'@'localhost' = PASSWORD('StrongRootPass123!');"
mysql -e "DELETE FROM mysql.user WHERE User='';"
mysql -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');"
mysql -e "DROP DATABASE IF EXISTS test;"
mysql -e "DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';"
mysql -e "FLUSH PRIVILEGES;"

# 4. Install WP-CLI (Command Line Interface for WordPress)
curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
chmod +x wp-cli.phar
mv wp-cli.phar /usr/local/bin/wp

# 5. Create directory for sites
mkdir -p /var/www/html

# 6. Set correct permissions
chown -R www-data:www-data /var/www/html

echo "✅ Server Setup Complete!"
echo "Now use 'bash add_site.sh domain.com' to deploy a new PBN site."
