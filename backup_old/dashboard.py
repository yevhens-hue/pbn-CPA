from flask import Flask, request
import sqlite3
import os
import datetime

app = Flask(__name__)

# Ensure data directory exists
DB_FILE = 'data/pbn_metrics.db'
if not os.path.exists('data'):
    os.makedirs('data')

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id TEXT,
            amount REAL,
            currency TEXT,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB on start
init_db()

@app.route('/postback', methods=['GET'])
def postback():
    try:
        # Get parameters from CPA network (using standard params, or custom mapping)
        # Assuming URL structure: ?sub1={post_id}&payout={amount}&status={status}&currency={currency}
        
        post_id = request.args.get('sub1')  # Internal Task/Row ID or WP Post ID
        amount = request.args.get('payout', 0.0) 
        status = request.args.get('status', 'unknown') # reg / dep
        currency = request.args.get('currency', 'USD')
        
        if not post_id:
            return "Missing sub1 (post_id)", 400

        # Log to DB
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Using current server time for simplicity, or could parse CPA timestamp if provided
        cursor.execute("INSERT INTO conversions (post_id, amount, currency, status, timestamp) VALUES (?, ?, ?, ?, datetime('now'))",
                       (post_id, float(amount), currency, status))
        
        conn.commit()
        conn.close()
        
        print(f"💰 Postback: ID={post_id}, Amount={amount} {currency}, Status={status}")
        return "OK", 200
        
    except Exception as e:
        print(f"❌ Postback Error: {e}")
        return "Error", 500

@app.route('/', methods=['GET'])
def health_check():
    return "PBN Dashboard Active 🚀", 200

if __name__ == '__main__':
    print("🚀 Starting PBN Dashboard (Postback Listener) on port 5001...")
    app.run(host='0.0.0.0', port=5001)
