print("Bot file loaded")

import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(msg.chat.id, "✅ Bot is working!")

bot.infinity_polling()
