from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time
import random
import os

BOT_TOKEN = '8640742680:AAEb8JeGfP4CyH1hiyrJBOrRLg827ZHc3c0'
CHAT_ID = -5549436048
AFFILIATE_TAG = 'wittyfinds-21'

bot = Bot(token=BOT_TOKEN)

DEALS = [
    ('Rucksack 70L', 'B08P53JH9Y', '🎒'),
    ('Powerbank 20000mAh', 'B0ABCDEFGH', '🔋'),
    ('Packing Cubes', 'B0XYZABCDE', '📦'),
]

def post_deals():
    try:
        deal = random.choice(DEALS)
        link = f"https://www.amazon.de/dp/{deal[1]}?tag={AFFILIATE_TAG}"
        msg = f"{deal[2]} *{deal[0]}*\n[→ ZUM DEAL]({link})\n#amazon #deals"
        bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")
        print(f"✅ Posted!")
    except Exception as e:
        print(f"Error: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(post_deals, 'interval', minutes=15)
scheduler.start()

print("✅ Bot running!")

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    pass
