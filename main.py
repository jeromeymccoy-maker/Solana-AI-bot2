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
