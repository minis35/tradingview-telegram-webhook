from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Telegram Bot bilgilerinizi buraya girin
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'BURAYA_BOT_TOKEN_YAZIN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', 'BURAYA_CHAT_ID_YAZIN')

def send_telegram_message(message):
    """Telegram'a mesaj gönder"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"Hata: {e}")
        return None

@app.route('/')
def home():
    return "TradingView Webhook Servisi Çalışıyor! ✅"

@app.route('/webhook', methods=['POST'])
def webhook():
    """TradingView'dan gelen webhook'u işle"""
    try:
        # TradingView'dan gelen veriyi al
        data = request.get_json()
        
        # Eğer metin formatında gelirse
        if not data:
            data = request.data.decode('utf-8')
        
        # Mesajı formatla
        if isinstance(data, dict):
            message = f"🔔 <b>TradingView Alarmı</b>\n\n"
            for key, value in data.items():
                message += f"<b>{key}:</b> {value}\n"
        else:
            message = f"🔔 <b>TradingView Alarmı</b>\n\n{data}"
        
        # Telegram'a gönder
        result = send_telegram_message(message)
        
        if result:
            return jsonify({"status": "success", "message": "Mesaj gönderildi"}), 200
        else:
            return jsonify({"status": "error", "message": "Telegram'a gönderilemedi"}), 500
            
    except Exception as e:
        print(f"Hata: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    """Test mesajı gönder"""
    message = "✅ Test mesajı - Webhook servisi çalışıyor!"
    result = send_telegram_message(message)
    if result:
        return jsonify({"status": "success", "message": "Test mesajı gönderildi"})
    else:
        return jsonify({"status": "error", "message": "Mesaj gönderilemedi"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
