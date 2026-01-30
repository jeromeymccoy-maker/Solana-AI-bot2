import telebot
import requests
import os

TOKEN = os.getenv("BOT_TOKEN")

TARGET_TOKEN = "Duj5mm4pyY6E4RXGpN4oVGtvVns5AzBYGknxTVYnpump"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🚀 Solana AI Bot Active\n"
        "Mode: Semi-Auto\n\n"
        "Commands:\n"
        "/price\n/status\n/analyze\n/help"
    )


@bot.message_handler(commands=["help"])
def help_cmd(msg):
    bot.send_message(
        msg.chat.id,
        "/price - Token price\n"
        "/status - Bot status\n"
        "/analyze - Market view"
    )


@bot.message_handler(commands=["status"])
def status(msg):
    bot.send_message(msg.chat.id, "✅ Running (Railway Cloud)")


@bot.message_handler(commands=["price"])
def price(msg):
    try:
        url = f"https://api.dexscreener.com/latest/dex/tokens/{TARGET_TOKEN}"
        r = requests.get(url).json()

        pair = r["pairs"][0]
        price = pair["priceUsd"]

        bot.send_message(
            msg.chat.id,
            f"💰 Token Price: ${price}"
        )
    except:
        bot.send_message(msg.chat.id, "⚠️ Price unavailable")


@bot.message_handler(commands=["analyze"])
def analyze(msg):
    bot.send_message(
        msg.chat.id,
        "📊 Analysis\n"
        "Trend: Neutral\n"
        "Momentum: Medium\n"
        "Risk: Moderate\n\n"
        "Recommendation: Wait for volume."
    )


print("Bot started...")
bot.infinity_polling()
