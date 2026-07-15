import requests
import time
import random
from datetime import datetime

BOT_TOKEN = '8640742680:AAEb8JeGfP4CyH1hiyrJBOrRLg827ZHc3c0'
CHAT_ID = -5549436048
AFFILIATE_TAG = 'wittyfinds-21'

DEALS = [
    ('Rucksack 70L', 'B08P53JH9Y', '🎒'),
    ('Powerbank 20000mAh', 'B0ABCDEFGH', '🔋'),
    ('Packing Cubes', 'B0XYZABCDE', '📦'),
    ('USB-C Adapter', 'B012345678', '🔌'),
    ('Reisekissen', 'B0QWERTY12', '🛏️'),
    ('Solar Powerbank', 'B0SOLAR001', '☀️'),
]

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': CHAT_ID,
        'text': text,
        'parse_mode': 'Markdown'
    }
    try:
        response = requests.post(url, data=data, timeout=5)
        if response.status_code == 200:
            print(f"✅ Nachricht gepostet!")
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
    return False

def post_deal():
    deal_title, asin, emoji = random.choice(DEALS)
    link = f"https://www.amazon.de/dp/{asin}?tag={AFFILIATE_TAG}"
    
    msg = f"{emoji} *{deal_title}*\n"
    msg += f"[→ ZUM DEAL]({link})\n"
    msg += f"⏰ {datetime.now().strftime('%H:%M')}\n"
    msg += "#amazon #deals"
    
    send_message(msg)

print("✅ Bot gestartet!")

# Alle 15 Min posten
counter = 0
while True:
    if counter % 180 == 0:  # 180 x 5 Sekunden = 15 Min
        post_deal()
    counter += 1
    time.sleep(5)
