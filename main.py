from telegram import Bot
import time

BOT_TOKEN = '8640742680:AAEb8JeGfP4CyH1hiyrJBOrRLg827ZHc3c0'
CHAT_ID = -5549436048

bot = Bot(token=BOT_TOKEN)

try:
    bot.send_message(chat_id=CHAT_ID, text="🤖 Bot Test - Funktioniert!")
    print("✅ TEST ERFOLGREICH!")
except Exception as e:
    print(f"❌ FEHLER: {e}")

while True:
    time.sleep(10)
