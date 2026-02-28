# How to Install the High-Roller Plugin

Since you cannot run server commands directly from your local machine, please follow these steps to install the plugin via the WordPress Admin Panel.

## 1. Download the Plugin
The plugin file is located at:
`PBN_Automation_Final/pbn-high-roller-plugin.zip`

## 2. Access WordPress Admin
1.  Open your web browser.
2.  Go to your WordPress Admin URL (e.g., `your-site.com/wp-admin`).
3.  Log in with your credentials.

## 3. Upload and Activate
1.  Navigate to **Plugins** -> **Add New** in the sidebar.
2.  Click the **Upload Plugin** button at the top.
3.  Choose the `pbn-high-roller-plugin.zip` file.
4.  Click **Install Now**.
5.  After installation, click **Activate Plugin**.

## 🎉 Done!
Your site will now automatically use the High-Roller theme styles and glassmorphism effects. No manual file editing or server permissions needed!

## ⚠️ Troubleshooting (Permissions Error)
If you see an error like `Could not create directory` during upload, your server permissions are incorrect. You must run these commands **on your server via SSH** (NOT in Cursor):

### Option 1: One-liner Command (Run this from your local terminal)
Copy and paste this entire command into your local terminal (where you are running `source ...`):

```bash
ssh root@95.217.163.88 "chown -R www-data:www-data /var/www/html/luckybetvip.com/wp-content/ && chmod -R 755 /var/www/html/luckybetvip.com/wp-content/"
```

### Option 2: Manual SSH Connection
If the above fails, log in first:
```bash
# Connect to your server (replace user and IP)
ssh root@95.217.163.88

# Run these commands to fix permissions
chown -R www-data:www-data /var/www/html/luckybetvip.com/wp-content/
chmod -R 755 /var/www/html/luckybetvip.com/wp-content/
```
After running these, try uploading the plugin again.
