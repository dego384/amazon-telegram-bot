from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time
import random
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN', '8640742680:AAEb8JeGfP4CyH1hiyrJBOrRLg827ZHc3c0')
CHAT_ID = int(os.environ.get('CHAT_ID', '-5549436048'))
AFFILIATE_TAG = os.environ.get('AFFILIATE_TAG', 'wittyfinds-21')

bot = Bot(token=BOT_TOKEN)
AMAZON_DEALS_URL = "https://www.amazon.de/deals"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def scrape_amazon_deals():
    try:
        response = requests.get(AMAZON_DEALS_URL, headers=HEADERS, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'lxml')
        deals = []
        deal_items = soup.find_all('div', {'class': 'a-section'})[:10]
        for item in deal_items:
            try:
                title_elem = item.find('span', {'class': 'a-size-base-plus'})
                title = title_elem.text.strip() if title_elem else "Produkt"
                price_elem = item.find('span', {'class': 'a-price-whole'})
                price = price_elem.text.strip() if price_elem else "N/A"
                asin_elem = item.find('a', {'class': 'a-link-normal'})
                if asin_elem and 'href' in asin_elem.attrs:
                    link = asin_elem['href']
                    if '/dp/' in link:
                        asin = link.split('/dp/')[1].split('/')[0]
                    else:
                        continue
                else:
                    continue
                if asin and len(title) > 5:
                    deals.append({'title': title[:70], 'price': price, 'asin': asin, 'emoji': random.choice(['🔥', '⚡', '💰', '🎁'])})
            except:
                continue
        return deals
    except Exception as e:
        print(f"❌ Scraping Fehler: {e}")
        return []

def generate_affiliate_link(asin):
    return f"https://www.amazon.de/dp/{asin}?tag={AFFILIATE_TAG}"

def post_deals():
    print(f"🔍 Scrape Amazon um {datetime.now()}")
    deals = scrape_amazon_deals()
    if not deals:
        print("❌ Keine Deals gefunden")
        return
    message = "🔥 *AMAZON DEALS* 🔥\n\n"
    for i, deal in enumerate(deals[:5], 1):
        affiliate_link = generate_affiliate_link(deal['asin'])
        message += f"{deal['emoji']} *Deal #{i}*\n"
        message += f"*{deal['title']}*\n"
        message += f"💰 *{deal['price']}*\n"
        message += f"[→ JETZT KAUFEN]({affiliate_link})\n\n"
    message += f"⏰ {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
    message += f"#amazon #deals #shopping"
    try:
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
        print(f"✅ {len(deals)} Deals gepostet")
    except Exception as e:
        print(f"❌ Fehler beim Posten: {e}")

scheduler = BackgroundScheduler(timezone='Europe/Berlin')
scheduler.add_job(post_deals, 'cron', hour=9, minute=0)
scheduler.add_job(post_deals, 'cron', hour=15, minute=0)
scheduler.start()

print("✅ Amazon Bot auf Railway läuft!")
print("Nächster Scrape um 09:00 Uhr")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    scheduler.shutdown()
    print("Bot gestoppt")
