import os
import telebot
import requests
import time

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
HELIUS_KEY = os.getenv("HELIUS_API_KEY", "").strip()

WALLET = "5JRoTbZKpzxPVsH22ngJj31nWQuuLxpSWpDTubMvRDKY"

bot = telebot.TeleBot(BOT_TOKEN)


def get_balance():
    url = "https://rpc.helius.xyz/?api-key=" + HELIUS_KEY

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [WALLET]
    }

    r = requests.post(url, json=payload, timeout=10).json()
    return r["result"]["value"] / 1e9


def get_recent():
    url = f"https://api.helius.xyz/v0/addresses/{WALLET}/transactions?api-key={HELIUS_KEY}"
    return requests.get(url, timeout=10).json()[:5]


@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(
        m.chat.id,
        "🚀 Crypto Bot Online\n"
        "/balance\n"
        "/recent"
    )


@bot.message_handler(commands=["balance"])
def balance(m):
    try:
        bal = get_balance()
        bot.send_message(m.chat.id, f"👛 Balance: {bal:.4f} SOL")
    except Exception as e:
        bot.send_message(m.chat.id, "⚠️ Balance error")


@bot.message_handler(commands=["recent"])
def recent(m):
    try:
        txs = get_recent()
        msg = "📜 Recent TXs:\n"

        for t in txs:
            msg += t["signature"][:20] + "...\n"

        bot.send_message(m.chat.id, msg)
    except:
        bot.send_message(m.chat.id, "⚠️ TX error")


print("Bot started...")
bot.infinity_polling()
import time
import threading

PROMO_MESSAGES = [
    "❄️🐉 $LVZ — Leviathanzilla is awakening! Join Leviathanzilla",
    "Early $LVZ holders = future legends 💎",
    "Next Solana dragon? Leviathanzilla 🐉",
    "Ice Dragon > Paper Hands ❄️💎",
    "Missed BONK? Don’t miss $LVZ 🚀"
]

CHAT_ID = "YOUR_TELEGRAM_GROUP_ID"


def auto_promote():
    while True:
        for msg in PROMO_MESSAGES:
            bot.send_message(CHAT_ID, msg)
            
            time.sleep(3600)  # 1 hour


threading.Thread(target=auto_promote).start()
@bot.message_handler(commands=['id'])
def get_id(message):
    bot.reply_to(message, f"Group ID: {message.chat.id}")
import time
import threading

PROMO_MESSAGES = [
    "❄️🐉 $LVZ — Leviathanzilla is awakening! Join now!",
    "Early $LVZ holders = future legends 💎 #LVZ",
    "Next Solana Ice Dragon? Leviathanzilla 🐉❄️",
    "Ice Dragon > Paper Hands ❄️💎 $LVZ",
    "Missed BONK? Don’t miss $LVZ 🚀"
]

CHAT_ID = -5194041530


def auto_promote():
    while True:
        for msg in PROMO_MESSAGES:
            try:
                bot.send_message(CHAT_ID, msg)
                time.sleep(3600)  # 1 hour
            except Exception as e:
                print("Promo error:", e)
                time.sleep(60)

@bot.message_handler(commands=['shill'])
def shill(message):
    bot.send_message(CHAT_ID, PROMO_MESSAGES[0])

threading.Thread(target=auto_promote, daemon=True).start()
def get_sol_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
    r = requests.get(url, timeout=10).json()
    return r["solana"]["usd"]
    price = get_sol_price()
usd = round(0.15 * price, 2)
import os
import telebot

# Get bot token from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing")

# Create bot
bot = telebot.TeleBot(BOT_TOKEN)

# Your chat ID (replace with yours)
CHAT_ID = "YOUR_CHAT_ID"

# Example values
usd = 25.50

# Message
msg = f"""
🚨 SNIPER ALERT 🚨

Token: LVZ

Buy: 0.15 SOL (~${usd})
Entry: $0.00012

Target: 20%
TP: $0.00018

Stop: 10%
SL: $0.00010

Risk: Low
"""

# Send message
bot.send_message(CHAT_ID, msg)

print("Alert sent!")
import os
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        f"Your Chat ID is: {message.chat.id}"
    )

print("Bot is running...")
bot.polling()
import requests
import telebot
import schedule
import time

# ======================
# CONFIGURATION
# ======================

# ← REPLACE THIS with your Telegram Bot Token from BotFather
BOT_TOKEN = 8364191087:AAHLZ_U8BhFxS358KnH14M3U51z75RF_HdI

# ← REPLACE THIS with your Telegram Chat ID from @userinfobot
CHAT_ID =938702556

# Token Info
TOKEN_NAME = "Leviathanzilla"
SYMBOL = "❄️🐉"
CHAIN = "Solana"
CONTRACT = "Duj5mm4pyY6E4RXGpN4oVGtvVns5AzBYGknxTVYnpump"

# DexScreener API (price/volume)
DEX_API = f"https://api.dexscreener.com/latest/dex/tokens/{CONTRACT}"

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# ======================
# FUNCTION: Check Price
# ======================

def check_price():
    try:
        r = requests.get(DEX_API)
        if r.status_code != 200:
            print("Error fetching data from DexScreener")
            return

        data = r.json()
        pairs = data.get("pairs")

        if not pairs:
            print("No trading pairs found")
            return

        pair = pairs[0]
        price = pair.get("priceUsd", "N/A")
        vol = pair.get("volume", {}).get("h24", "N/A")

        # Message to send to Telegram
        msg = f"""
❄️🐉 Leviathanzilla Update

💰 Price: ${price}
📊 24h Volume: {vol}
🔗 Contract: {CONTRACT}

Join our Telegram: t.me/Leviathanzilla
"""
        bot.send_message(CHAT_ID, msg)
        print("Update sent to Telegram!")

    except Exception as e:
        print(f"Error: {e}")

# ======================
# SCHEDULER
# ======================

# Check price every 30 minutes
schedule.every(30).minutes.do(check_price)

print("Leviathanzilla Bot Running...")
check_price()  # Run once immediately

while True:
    schedule.run_pending()
    time.sleep(10)
