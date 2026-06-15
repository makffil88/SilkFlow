import os
import random
import datetime
import logging

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from db import init_db, create_order, update_status, add_log

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPER_ADMIN_ID = int(os.getenv("SUPER_ADMIN_ID"))
ADMIN_IDS = set(int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x)

logging.basicConfig(level=logging.INFO)

user_state = {}

# ================= ROLE =================

def is_admin(user_id):
    return user_id == SUPER_ADMIN_ID or user_id in ADMIN_IDS

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 SilkFlow v6 ACTIVE")

# ================= CREATE ORDER =================

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if text == "new":
        user_state[user_id] = "WAIT_AMOUNT"
        await update.message.reply_text("💰 Введите сумму")
        return

    if user_state.get(user_id) == "WAIT_AMOUNT":
        try:
            amount = float(text)
            order_id = random.randint(10000, 99999)
            now = str(datetime.datetime.now())

            create_order(
                order_id,
                user_id,
                amount,
                "EXCHANGE",
                "NEW",
                now
            )

            user_state[user_id] = None

            await update.message.reply_text(
                f"✅ ORDER CREATED\nID: {order_id}"
            )

        except:
            await update.message.reply_text("❌ number only")

# ================= CALLBACK =================

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    action, order_id = q.data.split("_")
    user_id = q.from_user.id

    if not is_admin(user_id):
        await q.edit_message_text("⛔ no access")
        return

    if action == "in":
        update_status(order_id, "IN_PROGRESS", user_id)
        add_log(order_id, user_id, "TAKE")

    elif action == "ok":
        update_status(order_id, "COMPLETED", user_id)
        add_log(order_id, user_id, "DONE")

    elif action == "no":
        update_status(order_id, "CANCELLED", user_id)
        add_log(order_id, user_id, "CANCEL")

    await q.edit_message_text(f"✔ updated #{order_id}")

# ================= MAIN =================

def main():
    init_db()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.add_handler(CallbackQueryHandler(callback))

    print("🚀 BOT v6 RUNNING")
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()