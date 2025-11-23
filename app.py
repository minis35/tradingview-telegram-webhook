from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def send_telegram(text):
    url = "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage"
    try:
        requests.post(url, json={'chat_id': TELEGRAM_CHAT_ID, 'text': text})
    except Exception as e:
        print("Error: " + str(e))

@app.route('/')
def home():
    return "OK"

@app.route('/test')
def test():
    time_now = datetime.now().strftime('%H:%M:%S')
    send_telegram("Test OK\n" + time_now)
    return "Test message sent to Telegram"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        url_params = request.args.to_dict()
        data = request.get_json(silent=True) or {}
        data.update(url_params)
        raw = request.data.decode('utf-8') if request.data else ''
        
        pair = data.get('pair') or data.get('ticker') or 'UNKNOWN'
        price = data.get('price') or data.get('close') or '?'
        tf = data.get('tf') or data.get('interval') or '?'
        msg = data.get('message') or raw or 'Alert'
        
        time_now = datetime.now().strftime('%H:%M:%S')
        text = pair + "\n\n" + str(price) + "\n" + str(tf) + "\n" + time_now + "\n\n" + msg
        
        send_telegram(text)
        print("Alert: " + pair + " - " + str(price) + " - " + str(tf))
        
        return jsonify({'status': 'ok'}), 200
        
    except Exception as e:
        print("Error: " + str(e))
        return jsonify({'status': 'error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
