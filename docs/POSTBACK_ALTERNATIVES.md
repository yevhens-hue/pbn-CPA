# Postback & Tracking Alternatives

If running the Python server locally (`localhost:5001`) with a tunnel is inconvenient (requires the laptop to be on 24/7), here are the best alternatives:

## 1. Google Apps Script (Recommended - Free & Serverless)
**Use Google Sheets itself as the server.** You can deploy a small script in the Google Sheet editor that acts as a webhook.

### Steps:
1. Open your Google Sheet > Extensions > Apps Script.
2. Paste this code:

```javascript
function doGet(e) {
  // Get Parameters from URL
  var p = e.parameter;
  var sub1 = p.sub1 || "Unknown";
  var payout = p.payout || 0;
  var status = p.status || "Unknown";
  var currency = p.currency || "USD";
  
  // Save to "Conversions" sheet
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Conversions");
  if (!sheet) {
    sheet = SpreadsheetApp.getActiveSpreadsheet().insertSheet("Conversions");
    sheet.appendRow(["Timestamp", "Post ID (sub1)", "Payout", "Currency", "Status"]);
  }
  
  sheet.appendRow([new Date(), sub1, payout, currency, status]);
  
  return ContentService.createTextOutput("OK").setMimeType(ContentService.MimeType.TEXT);
}
```

3. Click **Deploy** > **New Deployment** > Select type: **Web app**.
4. Set "Who has access" to **Anyone**.
5. Copy the URL (starts with `script.google.com/...`).

**Your new Postback URL:**
`https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec?sub1={sub1}&payout={payout}&status={status}&currency={currency}`

*Pros:* No server needed, zero cost, data goes directly to sheet.
*Cons:* Slightly slower response time (OK for postbacks).

---

## 2. Cloud Server (VPS) - Professional
Rent a cheap Linux server ($3-5/mo) on DigitalOcean, Hetzner, or AWS.

### Steps:
1. Upload your `dashboard.py` and `requirements.txt`.
2. Run it with `gunicorn` or `systemd` to keep it alive 24/7.
3. Use the server's static IP.

*Pros:* Extremely fast, professional, can host multiple bots.
*Cons:* Monthly cost, requires Linux maintenance.

---

## 3. Render / Railway / Heroku (PaaS)
Deploy the Python `dashboard.py` to a platform-as-a-service.

### Steps:
1. Push code to GitHub.
2. Connect GitHub repo to Render.com (free tier available).
3. It gives you a `https://your-app.onrender.com` URL.

*Pros:* Easy deployment, HTTPS handled automatically.
*Cons:* Free tiers sleep after inactivity (missed postbacks), paid tiers cost money.

---

## Recommendation
Since you already use Google Sheets heavily, **Option 1 (Google Apps Script)** is the easiest path. It keeps your workflow centralized and requires zero maintenance.
