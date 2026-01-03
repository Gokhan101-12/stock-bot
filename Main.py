import yfinance as yf
import requests
import os

# --- AYARLAR ---
# GitHub Secrets'tan veya direkt buraya yazabilirsin (Güvenlik için Secrets önerilir)
BOT_TOKEN = 8201264694: AAG_E7j_RvaCCX@WlMokf×gTQ
VpNvBmchYc
CHAT_ID = 1123565558
PORTFOY = ["THYAO.IS", "EREGL.IS", "FROTO.IS"] # İzlenecek hisseler

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def analyze_and_report():
    report = "📊 **GÜNLÜK BORSA RAPORU** 📊\n\n"
    
    for symbol in PORTFOY:
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            fiyat = info.get('currentPrice', 0)
            fk = info.get('trailingPE', 0)
            
            # Basit Graham Değerlemesi
            eps = info.get('trailingEps', 0)
            fair_value = eps * (8.5 + 2 * 15) if eps > 0 else 0
            potansiyel = ((fair_value - fiyat) / fiyat * 100) if fair_value > 0 else 0
            
            # Sinyal Emojisi
            signal = "🟢 AL" if potansiyel > 30 else "🔴 SAT" if potansiyel < 0 else "🟡 TUT"

            report += f"*{symbol}* ({fiyat} TL)\n"
            report += f"F/K: {fk:.2f} | Potansiyel: %{potansiyel:.1f}\n"
            report += f"Sinyal: {signal}\n------------------\n"
        except Exception as e:
            report += f"⚠️ {symbol} verisi çekilemedi.\n"
            
    send_telegram(report)

if __name__ == "__main__":
    analyze_and_report()
