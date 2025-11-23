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
        print(f"Telegram gönderim hatası: {e}")
        return None

@app.route('/')
def home():
    return "TradingView Webhook Servisi Çalışıyor! ✅"

@app.route('/webhook', methods=['POST'])
def webhook():
    """TradingView'dan gelen webhook'u işle"""
    try:
        # URL parametrelerini al
        url_params = request.args.to_dict()
        
        # POST verisini al
        data = {}
        raw_data = request.data.decode('utf-8')
        
        print(f"🔍 Raw data: {raw_data}")
        print(f"🔍 Content-Type: {request.content_type}")
        
        # Önce JSON olarak parse et
        try:
            if request.is_json:
                data = request.get_json(force=True)
            else:
                # JSON değilse string olarak gelmiş olabilir
                if raw_data:
                    try:
                        data = json.loads(raw_data)
                    except:
                        data = {'raw_message': raw_data}
        except Exception as e:
            print(f"⚠️ JSON parse hatası: {e}")
            data = {'raw_message': raw_data}
        
        # URL parametrelerini ekle
        data.update(url_params)
        
        print(f"📥 Parsed data: {data}")
        
        # Bilgileri çıkar
        pair = (data.get('ticker') or 
                data.get('pair') or 
                data.get('symbol') or 
                'UNKNOWN')
        
        price = (data.get('close') or 
                 data.get('price') or 
                 '?')
        
        timeframe = (data.get('interval') or 
                     data.get('timeframe') or 
                     data.get('tf') or 
                     '?')
        
        time_str = data.get('time') or datetime.now().strftime('%H:%M:%S')
        
        # Alarm mesajını al
        alert_msg = (data.get('message') or 
                    data.get('alert') or 
                    data.get('alert_name') or 
                    data.get('raw_message') or 
                    'Alert Triggered')
        
        # Telegram mesajını oluştur
        message = f"""🔔 <b>{pair}</b>

💰 {price}
⏱ {timeframe}
🕐 {time_str}

{alert_msg}"""
        
        # Console log
        print(f"✅ Alarm: {pair} - {price} - {timeframe}")
        
        # Telegram'a gönder
        result = send_telegram_message(message)
        
        if result:
            return jsonify({"status": "success", "message": "Mesaj gönderildi"}), 200
        else:
            return jsonify({"status": "error", "message": "Telegram'a gönderilemedi"}), 500
            
    except Exception as e:
        print(f"❌ Webhook hatası: {e}")
        
        # Hata durumunda bile basit mesaj gönder
        try:
            error_msg = f"⚠️ <b>Webhook Hatası</b>\n\n{str(e)}\n\nHam veri:\n<code>{request.data.decode('utf-8')}</code>"
            send_telegram_message(error_msg)
        except:
            pass
        
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    """Test mesajı gönder"""
    test_msg = f"""✅ <b>Test Mesajı</b>

Server çalışıyor!
🕐 {datetime.now().strftime('%H:%M:%S')}"""
    
    result = send_telegram_message(test_msg)
    
    if result:
        return jsonify({"status": "success", "message": "Test mesajı gönderildi"})
    else:
        return jsonify({"status": "error", "message": "Mesaj gönderilemedi"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

---

## 🔄 KODU GÜNCELLE

### **GitHub'da:**

1. **app.py'yi aç**
2. **Tüm içeriği yukarıdaki kodla değiştir**
3. **Commit message:** "Add better JSON parsing and logging"
4. **Commit changes**

### **Render deploy edecek (1-2 dk)**

---

## 🔍 SONRA TEST VE LOG KONTROL

### **1. Test Alarm Gönder**

TradingView'dan test et.

### **2. Render Logs'u İzle**

**Göreceğin loglar:**
```
🔍 Raw data: {"ticker":"BTCUSDT","close":"98450.50",...}
🔍 Content-Type: application/json
📥 Parsed data: {'ticker': 'BTCUSDT', 'close': '98450.50', 'interval': '15m', ...}
✅ Alarm: BTCUSDT - 98450.50 - 15m
```

### **3. Telegram'ı Kontrol Et**
```
🔔 BTCUSDT

💰 98,450.50
⏱ 15m
🕐 16:55:23

Bearish SMT with BTC.D CONFIRMED
