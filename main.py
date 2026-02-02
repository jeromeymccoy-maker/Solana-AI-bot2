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
ADMIN_IDS = [938702556]  # <- REPLACE WITH YOUR ID

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
    AUTO_CHAT_ID = -1001234567890  # <- REPLACE

    # Start auto-post thread
    t = threading.Thread(target=auto_price_post)
    t.daemon = True
    t.start()

    # Run bot
    run_bot()
