# -*- coding: utf-8 -*-
import telebot, os, sqlite3, threading, time, requests
from telebot import types
from flask import Flask
from datetime import datetime
import psutil

# ---------- CONFIG ----------
TOKEN = "7760716416:AAHktoCqDuRDv9JbCV6S10ZkMOUasx1EPPo"  # <-- Yahan apna Telegram bot token daal
OWNER_ID = 7845479937
FORCE_CHANNEL = "@pfp_kahi_nhi_milega"  # <-- Yahan apna channel username daal
CHANNEL_LINK = "https://t.me/pfp_kahi_nhi_milega"  # <-- Yahan apna channel link daal
# ----------------------------

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "I'm Alive ✅"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# ---------- FORCE JOIN CHECK ----------
def is_user_joined(user_id):
    try:
        member = bot.get_chat_member(FORCE_CHANNEL, user_id)
        if member.status in ["creator", "administrator", "member"]:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False

# ---------- START COMMAND ----------
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    first = message.from_user.first_name

    if not is_user_joined(user_id):
        markup = types.InlineKeyboardMarkup()
        join_btn = types.InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)
        refresh_btn = types.InlineKeyboardButton("✅ I've Joined", callback_data="refresh")
        markup.add(join_btn)
        markup.add(refresh_btn)
        bot.reply_to(
            message,
            f"⚠️ Hello {first}!\n\nYou must join our updates channel to use this bot.\n\n👉 [Join Here]({CHANNEL_LINK}) and press **'I've Joined'** button.",
            parse_mode="Markdown",
            reply_markup=markup,
        )
        return

    # If user joined
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📤 Upload File", "📂 Check Files")
    markup.add("⚡ Bot Speed", "📞 Contact Owner")
    bot.reply_to(
        message,
        f"👋 Welcome, {first}!\n\nYou're verified ✅\nUse the menu below to interact with the bot.",
        reply_markup=markup,
    )

# ---------- REFRESH CALLBACK ----------
@bot.callback_query_handler(func=lambda call: call.data == "refresh")
def refresh(call):
    user_id = call.from_user.id
    if is_user_joined(user_id):
        bot.answer_callback_query(call.id, "✅ Verified! Access granted.")
        bot.send_message(
            call.message.chat.id,
            "✅ You have successfully joined the channel!\nNow you can use all bot features.",
        )
        bot.send_message(call.message.chat.id, "Type /start again 👇")
    else:
        bot.answer_callback_query(call.id, "⚠️ You haven't joined yet!")
        bot.send_message(
            call.message.chat.id,
            f"❌ Please join our channel first.\n👉 {CHANNEL_LINK}",
        )

# ---------- SPEED TEST ----------
@bot.message_handler(func=lambda msg: msg.text == "⚡ Bot Speed")
def speed_test(message):
    start = time.time()
    msg = bot.reply_to(message, "Testing speed...")
    end = time.time()
    bot.edit_message_text(
        f"⚡ Response Time: {round((end - start) * 1000, 2)} ms",
        chat_id=message.chat.id,
        message_id=msg.message_id,
    )

# ---------- CONTACT ----------
@bot.message_handler(func=lambda msg: msg.text == "📞 Contact Owner")
def contact_owner(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📞 Contact Owner", url=f"https://t.me/R4HULxTRUSTED"))
    bot.reply_to(message, "Need help? Contact below 👇", reply_markup=markup)

# ---------- UPLOAD & FILE BUTTONS PLACEHOLDER ----------
@bot.message_handler(func=lambda msg: msg.text in ["📤 Upload File", "📂 Check Files"])
def coming_soon(message):
    bot.reply_to(message, "⚙️ Full file upload system already included in main bot.\nThis is demo force-join setup ✅")

# ---------- RUN ----------
keep_alive()
print("Bot started successfully ✅")
bot.infinity_polling(skip_pending=True)
