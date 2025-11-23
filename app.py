from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={'chat_id': TELEGRAM_CHAT_ID, 'text': text, 'parse_mode': 'HTML'})
    except Exception as e:
        print(f"Telegram error: {e}")

@app.route('/')
def home():
    return "Webhook Active"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Get URL parameters
        url_params = request.args.to_dict()
        
        # Get POST data
        data = request.get_json(silent=True) or {}
        data.update(url_params)
        
        # Get raw data as fallback
        raw = request.data.decode('utf-8') if request.data else ''
        
        # Extract info
        pair = data.get('pair') or data.get('ticker') or data.get('symbol') or 'UNKNOWN'
        price = data.get('price') or data.get('close') or '?'
        tf = data.get('tf') or data.get('interval') or data.get('timeframe') or '?'
        msg = data.get('message') or data.get('alert') or raw or 'Alert'
        
        # Create message
        time_now = datetime.now().strftime('%H:%M:%S')
        text = f"<b>{pair}</b>\n\n{price}\n{tf}\n{time_now}\n\n{msg}"
        
        # Send to Telegram
        send_telegram(text)
        
        # Log
        print(f"Alert: {pair} - {price} - {tf}")
        
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    time_now = datetime.now().strftime('%H:%M:%S')
    send_telegram(f"<b>Test OK</b>\n\n{time_now}")
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

---

## 🔄 DEPLOY

1. **GitHub'da app.py'yi aç**
2. **Tüm içeriği sil**
3. **Yukarıdaki kodu yapıştır**
4. **Commit: "Remove emojis from code"**
5. **Commit changes**

---

## ⏱️ 1-2 DAKİKA BEKLE

Render otomatik deploy edecek.

**"Live"** olunca test et:
```
https://tradingview-telegram-webhook.onrender.com/test
```

**Telegram'a gelecek:**
```
Test OK

17:35:42
