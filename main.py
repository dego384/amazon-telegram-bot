from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import feedparser
import requests
import time
import random
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN', '8640742680:AAEb8JeGfP4CyH1hiyrJBOrRLg827ZHc3c0')
CHAT_ID = int(os.environ.get('CHAT_ID', '-5549436048'))
AFFILIATE_TAG = os.environ.get('AFFILIATE_TAG', 'wittyfinds-21')

bot = Bot(token=BOT_TOKEN)

# Deutsche Deal-Feeds (öffentlich verfügbar)
RSS_FEEDS = [
    "https://www.mydealz.de/rss/deals/hot",  # MyDealz Hot Deals
    "https://www.dealshare.de/feed/rss",     # DealShare
]

def get_deals_from_feeds():
    """Liest Deals von RSS-Feeds"""
    try:
        all_deals = []
        
        for feed_url in RSS_FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                entries = feed.entries[:5]  # Top 5 pro Feed
                
                for entry in entries:
                    title = entry.get('title', 'Deal')
                    link = entry.get('link', '')
                    
                    # Nur Amazon-Links verarbeiten
                    if 'amazon' in link.lower():
                        # ASIN aus Link extrahieren
                        if '/dp/' in link:
                            asin = link.split('/dp/')[1].split('/')[0]
                            
                            # Mit Affiliate-Tag ersetzen
                            affiliate_link = f"https://www.amazon.de/dp/{asin}?tag={AFFILIATE_TAG}"
                            
                            all_deals.append({
                                'title': title[:80],
                                'link': affiliate_link,
                                'emoji': random.choice(['🔥', '⚡', '💰', '🎁', '✨'])
                            })
            except Exception as e:
                print(f"Feed-Fehler: {e}")
                continue
        
        return all_deals
    except Exception as e:
        print(f"❌ Feed-Fehler: {e}")
        return []

def post_deals():
    """Postet Deals auf Telegram"""
    print(f"🔍 Hole Deals von RSS-Feeds um {datetime.now()}")
    
    deals = get_deals_from_feeds()
    
    if not deals:
        print("❌ Keine Deals gefunden")
        return
    
    message = "🔥 *AMAZON DEALS* 🔥\n\n"
    
    for i, deal in enumerate(deals[:5], 1):
        message += f"{deal['emoji']} *Deal #{i}*\n"
        message += f"*{deal['title']}*\n"
        message += f"[→ ZUM DEAL]({deal['link']})\n\n"
    
    message += f"⏰ {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
    message += f"#amazon #deals #schnäppchen"
    
    try:
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
        print(f"✅ {len(deals)} Deals gepostet")
    except Exception as e:
        print(f"❌ Fehler beim Posten: {e}")

scheduler = BackgroundScheduler(timezone='Europe/Berlin')

# ALLE 15 MINUTEN!!!
scheduler.add_job(post_deals, 'interval', minutes=15)

scheduler.start()

print("✅ RSS-Feed Bot läuft!")
print("📤 Postet ALLE 15 MINUTEN")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    scheduler.shutdown()
    print("Bot gestoppt")
