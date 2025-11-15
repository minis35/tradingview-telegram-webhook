# TradingView → Telegram Webhook Servisi

TradingView alarmlarınızı Telegram'a otomatik olarak gönderen basit webhook servisi.

## 🚀 Kurulum Adımları

### 1. Telegram Bot Oluşturma

1. Telegram'da **@BotFather**'ı arayın
2. `/newbot` komutunu gönderin
3. Bot ismi ve kullanıcı adı belirleyin
4. Size verilen **TOKEN**'ı kaydedin

### 2. Chat ID Öğrenme

1. Botunuza bir mesaj gönderin
2. Tarayıcıda şu adresi açın (TOKEN yerine kendi token'ınızı yazın):
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
3. JSON'da `"chat":{"id":` kısmındaki sayıyı kaydedin

### 3. Render.com'da Deploy (ÜCRETSİZ)

1. **render.com**'a git ve GitHub ile giriş yap
2. Bu projeyi GitHub'a yükle (veya Render'da "New Web Service" → "Public Git repository" seç)
3. **New** → **Web Service** tıkla
4. Repository'nizi seçin
5. Ayarları yapın:
   - **Name**: istediğiniz isim (örn: `tradingview-webhook`)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free`

6. **Environment Variables** (Ortam Değişkenleri) ekleyin:
   - `TELEGRAM_BOT_TOKEN`: Bot token'ınız
   - `TELEGRAM_CHAT_ID`: Chat ID'niz

7. **Create Web Service** tıklayın

### 4. Railway.app Alternatifi (ÜCRETSİZ)

1. **railway.app**'e git
2. GitHub ile giriş yap
3. **New Project** → **Deploy from GitHub repo**
4. Repository'nizi seçin
5. Environment Variables ekle:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
6. Deploy edilecek

### 5. Servisi Test Etme

Deploy edildikten sonra size bir URL verilecek (örn: `https://your-app.onrender.com`)

Test için tarayıcıda şunu açın:
```
https://your-app.onrender.com/test
```

Telegram'da test mesajı gelirse ✅ çalışıyor demektir!

### 6. TradingView'da Kullanma

1. TradingView'da bir alarm oluşturun
2. **Notifications** (Bildirimler) bölümünde **Webhook URL** aktif edin
3. URL olarak girin:
   ```
   https://your-app.onrender.com/webhook
   ```
4. **Message** alanına istediğiniz formatı yazın, örnek:
   ```json
   {
     "sembol": "{{ticker}}",
     "fiyat": "{{close}}",
     "zaman": "{{time}}",
     "mesaj": "{{strategy.order.action}} sinyali geldi!"
   }
   ```

## 📱 Kullanım

Artık TradingView alarmlarınız otomatik olarak Telegram'a gelecek!

## 🔧 Özelleştirme

`app.py` dosyasındaki `webhook()` fonksiyonunu düzenleyerek mesaj formatını değiştirebilirsiniz.

## ⚠️ Notlar

- Render.com ücretsiz planı 15 dakika hareketsizlikten sonra uyur, ilk istek 30 saniye sürebilir
- Railway.app aylık 5$ ücretsiz kredi verir
- Her ikisi de 7/24 çalışır

## 🆘 Sorun Giderme

**Mesaj gelmiyor mu?**
1. `/test` endpoint'ini kontrol edin
2. Render/Railway loglarını inceleyin
3. Bot TOKEN ve Chat ID'nin doğru olduğundan emin olun
4. TradingView webhook URL'sinin doğru olduğunu kontrol edin

## 📝 Lisans

MIT - İstediğiniz gibi kullanabilirsiniz!
