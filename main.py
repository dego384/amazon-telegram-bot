from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time
import random
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN', '8640742680:AAEb8JeGfP4CyH1hiyrJBOrRLg827ZHc3c0')
CHAT_ID = int(os.environ.get('CHAT_ID', '-5549436048'))
AFFILIATE_TAG = os.environ.get('AFFILIATE_TAG', 'wittyfinds-21')

bot = Bot(token=BOT_TOKEN)

SAMPLE_DEALS = [
    {'title': 'Rucksack 70L Bikepacking', 'asin': 'B08P53JH9Y', 'emoji': '🎒'},
    {'title': 'Powerbank 20000mAh', 'asin': 'B0ABCDEFGH', 'emoji': '🔋'},
    {'title': 'Packing Cubes Set (5er)', 'asin': 'B0XYZABCDE', 'emoji': '📦'},
    {'title': 'USB-C Reiseadapter', 'asin': 'B012345678', 'emoji': '🔌'},
    {'title': 'Elektronischer Gepäckwaage', 'asin': 'B0ASDFGHJK', 'emoji': '⚖️'},
    {'title': 'Reisekissen Memory Foam', 'asin': 'B0QWERTY12', 'emoji': '🛏️'},
    {'title': 'Kompression-Packing Cubes', 'asin': 'B0ZXCVBNM1', 'emoji': '📦'},
    {'title': 'Solar Powerbank 25W', 'asin': 'B0ASDFGH23', 'emoji': '☀️'},
]

def generate_affiliate_link(asin):
    return f"https://www.amazon.de/dp/{asin}?tag={AFFILIATE_TAG}"

def post_deals():
    print(f"📤 Poste Deals um {datetime.now()}")
    
    selected_deals = random.sample(SAMPLE_DEALS, min(5, len(SAMPLE_DEALS)))
    
    message = "🔥 *AMAZON DEALS* 🔥\n\n"
    
    for i, deal in enumerate(selected_deals, 1):
        affiliate_link = generate_affiliate_link(deal['asin'])
        message += f"{deal['emoji']} *Deal #{i}*\n"
        message += f"*{deal['title']}*\n"
        message += f"[→ ZUM DEAL]({affiliate_link})\n\n"
    
    message += f"⏰ {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
    message += f"#amazon #deals #schnäppchen"
    
    try:
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
        print(f"✅ Deals gepostet!")
    except Exception as e:
        print(f"❌ Fehler: {e}")

scheduler = BackgroundScheduler(timezone='Europe/Berlin')
scheduler.add_job(post_deals, 'interval', minutes=15)
scheduler.start()

print("✅ Bot läuft!")

while True:
    time.sleep(60)
