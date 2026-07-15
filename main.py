import asyncio
from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler
import time
import random

BOT_TOKEN = '...'
CHAT_ID = -5549436048
AFFILIATE_TAG = 'wittyfinds-21'

bot = Bot(token=BOT_TOKEN)

DEALS = [
    ('Rucksack 70L', 'B08P53JH9Y', '🎒'),
    ('Powerbank 20000mAh', 'B0ABCDEFGH', '🔋'),
    ('Packing Cubes', 'B0XYZABCDE', '📦'),
    ('USB-C Adapter', 'B012345678', '🔌'),
    ('Reisekissen', 'B0QWERTY12', '🛏️'),
]

async def send_deal():
    deal = random.choice(DEALS)
    link = f"https://www.amazon.de/dp/{deal[1]}?tag={AFFILIATE_TAG}"
    msg = f"{deal[2]} *{deal[0]}*\n[→ ZUM DEAL]({link})\n#amazon #deals"
    await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")

def post_deals():
    try:
        asyncio.run(send_deal())
        print("✅ Posted!")
    except Exception as e:
        print(f"❌ Fehler: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(post_deals, 'interval', minutes=15)
scheduler.start()

print("✅ Bot running!")
while True:
    time.sleep(60)
