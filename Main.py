import os
import telebot
import requests
from solana.publickey import PublicKey

# Load env vars
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
HEL_RPC = os.getenv("HELIUS_RPC_URL", "").strip()
TRACK_WALLET = "5JRoTbZKpzxPVsH22ngJj31nWQuuLxpSWpDTubMvRDKY"

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🚀 Solana AI Bot Ready! Commands:\n"
        "/balance - Wallet balance\n"
        "/recent - Recent txs\n"
        "/scan - Token scanner\n"
        "/help - Show commands"
    )


@bot.message_handler(commands=["help"])
def help_cmd(msg):
    bot.send_message(
        msg.chat.id,
        "/balance - Wallet balance\n"
        "/recent - Recent transactions\n"
        "/scan <min_vol> - Scan new tokens"
    )


@bot.message_handler(commands=["balance"])
def balance(msg):
    try:
        # Call Helius RPC for balance
        url = f"{HEL_RPC}&address={TRACK_WALLET}"
        res = requests.get(url).json()
        lamports = res.get("value", [{}])[0].get("balance", 0)
        sol_balance = lamports / 1e9

        bot.send_message(msg.chat.id, f"👛 Wallet Balance: {sol_balance} SOL")
    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Could not fetch balance")

    
@bot.message_handler(commands=["recent"])
def recent(msg):
    try:
        url = f"{HEL_RPC}&address={TRACK_WALLET}"
        data = requests.get(url).json()
        txs = data[:5]
        reply = "📜 Recent Transactions:\n"
        for tx in txs:
            sig = tx.get("signature")
            reply += f"- {sig}\n"
        bot.send_message(msg.chat.id, reply)
    except:
        bot.send_message(msg.chat.id, "⚠️ Cannot load recent txs")


@bot.message_handler(commands=["scan"])
def scan(msg):
    parts = msg.text.split()
    min_vol = float(parts[1]) if len(parts) > 1 else 1000
    # Temporary placeholder scanner (dummy response)
    bot.send_message(msg.chat.id,
                     f"🔍 Scanning tokens with min volume ≥ {min_vol} USDC...\n"
                     "Feature coming soon!")
    

bot.polling()
