from flask import Flask, request, jsonify
import requests
import os
import json
from datetime import datetime

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'BURAYA_BOT_TOKEN_YAZIN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', 'BURAYA_CHAT_ID_YAZIN')

def send_telegram_message(message):
    """Telegram'a mesaj gönder"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"Telegram error: {e}")
        return None

@app.route('/')
def home():
    return "TradingView Webhook Active"

@app.route('/webhook', methods=['POST'])
def webhook():
    """TradingView webhook handler"""
    try:
        # Get URL parameters
        url_params = request.args.to_dict()
        
        # Get POST data
        data = {}
        raw_data = request.data.decode('utf-8')
        
        print(f"Raw data: {raw_data}")
        print(f"Content-Type: {request.content_type}")
        
        # Parse JSON
        try:
            if request.is_json:
                data = request.get_json(force=True)
            else:
                if raw_data:
                    try:
                        data = json.loads(raw_data)
                    except:
                        data = {'raw_message': raw_data}
        except Exception as e:
            print(f"JSON parse error: {e}")
            data = {'raw_message': raw_data}
        
        # Add URL params
        data.update(url_params)
        
        print(f"Parsed data: {data}")
        
        # Extract info
        pair = data.get('ticker') or data.get('pair') or data.get('symbol') or 'UNKNOWN'
        price = data.get('close') or data.get('price') or '?'
        timeframe = data.get('interval') or data.get('timeframe') or data.get('tf') or '?'
        time_str = data.get('time') or datetime.now().strftime('%H:%M:%S')
        alert_msg = data.get('message') or data.get('alert') or data.get('alert_name') or data.get('raw_message') or 'Alert'
        
        # Create message
        message = f"<b>{pair}</b>\n\n{price}\n{timeframe}\n{time_str}\n\n{alert_msg}"
        
        print(f"Alert: {pair} - {price} - {timeframe}")
        
        # Send to Telegram
        result = send_telegram_message(message)
        
        if result:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error"}), 500
            
    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    """Test endpoint"""
    test_msg = f"Test OK\n{datetime.now().strftime('%H:%M:%S')}"
    result = send_telegram_message(test_msg)
    
    if result:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

---

## ✅ FARKLAR

1. ✅ Emoji'leri kaldırdım (syntax sorununu çözer)
2. ✅ Üç tırnak yerine tek satır string
3. ✅ Daha basit message formatı
4. ✅ Print statement'ları basitleştirdim

---

## 🔄 GÜNCELLE

### **GitHub'da:**

1. **app.py'yi aç**
2. **Tüm içeriği sil**
3. **Yukarıdaki kodu yapıştır**
4. **Commit: "Fix syntax error"**
5. **Commit changes**

### **Render 1-2 dakikada deploy eder**

---

## 🧪 TEST

Deploy tamamlanınca:
```
https://tradingview-telegram-webhook.onrender.com/test
```

**Beklenen Telegram:**
```
Test OK
17:05:23
