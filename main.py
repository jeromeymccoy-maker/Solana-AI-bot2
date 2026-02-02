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
import os
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing!")

bot = telebot.TeleBot(BOT_TOKEN)

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
import os
import telebot
from telebot.apihelper import ApiException

# Get the bot token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing!")

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# Set your chat ID (replace with your own chat ID)
CHAT_ID =938702556

# Function to send a test message
def send_startup_message():
    try:
        bot.send_message(CHAT_ID, "✅ Bot started successfully!")
        print("Startup message sent successfully.")
    except ApiException as e:
        print(f"Failed to send startup message: {e}")

# Call the startup message function
send_startup_message()

# Example: keep the bot running and listening for commands
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Hello! Bot is running.")

# Start polling (listening for messages)
if __name__ == "__main__":
    print("Bot is polling for messages...")
    bot.infinity_polling()
import os
import time
import telebot
from telebot.apihelper import ApiException, NetworkError

# Get the bot token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing!")

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# Replace with your actual Telegram chat ID
CHAT_ID =938702556

# Function to send a test message on startup
def send_startup_message():
    try:
        bot.send_message(CHAT_ID, "✅ Bot started successfully!")
        print("Startup message sent successfully.")
    except ApiException as e:
        print(f"Failed to send startup message: {e}")

# Call startup message
send_startup_message()

# Example command handler
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Hello! Bot is running.")

# Robust polling with automatic reconnect
def run_bot():
    while True:
        try:
            print("Bot is polling for messages...")
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except NetworkError as e:
            print(f"Network error occurred: {e}. Reconnecting in 5 seconds...")
            time.sleep(5)
        except ApiException as e:
            print(f"Telegram API error occurred: {e}. Reconnecting in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"Unexpected error: {e}. Reconnecting in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    run_bot()
import os
import time
import threading
import requests
import telebot
from telebot.apihelper import ApiException, NetworkError

# ================== CONFIG ==================

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing!")

# Put YOUR Telegram user ID here
ADMIN_IDS = [123456789]  # <- REPLACE WITH YOUR ID

# Group spam words (edit as you like)
SPAM_WORDS = ["scam", "free crypto", "airdrop", "click here", "dm me"]

# ================== BOT INIT ==================

bot = telebot.TeleBot(BOT_TOKEN, threaded=True)

# ================== HELPERS ==================

def is_admin(user_id):
    return user_id in ADMIN_IDS


def get_sol_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": "solana", "vs_currencies": "usd"}
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        return data["solana"]["usd"]
    except:
        return None


# ================== WELCOME ==================

@bot.message_handler(content_types=["new_chat_members"])
def welcome(message):
    for user in message.new_chat_members:
        bot.send_message(
            message.chat.id,
            f"👋 Welcome {user.first_name}!\nType /help to see commands."
        )


# ================== COMMANDS ==================

@bot.message_handler(commands=["start", "help"])
def help_cmd(message):
    bot.reply_to(
        message,
        """
🤖 Leviathanzilla Bot

Commands:
• balance
• recent
• /price
• /help

Admin:
• /announce
• /status
"""
    )


@bot.message_handler(commands=["price"])
def price(message):
    price = get_sol_price()

    if price:
        bot.reply_to(message, f"💰 SOL Price: ${price}")
    else:
        bot.reply_to(message, "❌ Failed to fetch price")


# ================== KEYWORDS ==================

@bot.message_handler(func=lambda m: m.text and "balance" in m.text.lower())
def balance(message):
    bot.reply_to(message, "💳 Balance: Coming soon")


@bot.message_handler(func=lambda m: m.text and "recent" in m.text.lower())
def recent(message):
    bot.reply_to(message, "📊 Recent trades: Coming soon")


# ================== ADMIN ==================

@bot.message_handler(commands=["announce"])
def announce(message):

    if not is_admin(message.from_user.id):
        return

    text = message.text.replace("/announce", "").strip()

    if not text:
        bot.reply_to(message, "Usage: /announce message")
        return

    bot.send_message(message.chat.id, f"📢 ANNOUNCEMENT:\n{text}")


@bot.message_handler(commands=["status"])
def status(message):

    if not is_admin(message.from_user.id):
        return

    bot.reply_to(message, "✅ Bot is running")


# ================== ANTI-SPAM ==================

@bot.message_handler(func=lambda m: m.text is not None)
def anti_spam(message):

    text = message.text.lower()

    for word in SPAM_WORDS:
        if word in text:
            try:
                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(
                    message.chat.id,
                    f"⚠️ Spam removed from {message.from_user.first_name}"
                )
            except:
                pass

            return


# ================== AUTO POSTS ==================

def auto_price_post():

    while True:

        try:
            price = get_sol_price()

            if price:
                bot.send_message(
                    AUTO_CHAT_ID,
                    f"⏰ Hourly SOL Update: ${price}"
                )

        except:
            pass

        time.sleep(3600)  # 1 hour


# ================== RUN ==================

def run_bot():

    while True:

        try:
            print("Bot running...")
            bot.infinity_polling(timeout=20, long_polling_timeout=10)

        except (NetworkError, ApiException) as e:
            print("Connection error:", e)
            time.sleep(5)

        except Exception as e:
            print("Crash:", e)
            time.sleep(5)


# ================== MAIN ==================

if __name__ == "__main__":

    # Put your group ID here for auto posts
    AUTO_CHAT_ID = #938702556 <- REPLACE

    # Start auto-post thread
    t = threading.Thread(target=auto_price_post)
    t.daemon = True
    t.start()

    # Run bot
    run_bot()
