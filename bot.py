from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

TOKEN = "8627019146:AAHWHiQKPQkNlPgvIyNC8fH5UOpn1NEfheE"

CHANNEL_ID = -1003902783949
QR_MESSAGE_ID = 10
ADMIN_ID = 7002005405

COMMON_VIDEO_ID = 8
HOW_TO_USE_VIDEO_ID = 12

# 🔹 FILES
SKIN_FULL_FILE = 3
SKIN_TEST_FILE = 3
ESP_FULL_FILE = 9
ESP_TEST_FILE = 9

# 🔹 KEYS
SKIN_FULL_KEY = "SKIN-FULL-KEY"
SKIN_TEST_KEY = "SKIN-TEST-KEY"
ESP_FULL_KEY = "ESP-FULL-KEY"
ESP_TEST_KEY = "ESP-TEST-KEY"

users = {}
pending = {}  # 🔥 payment temp data


def get_user(uid):
    if uid not in users:
        users[uid] = {"balance": 0}
    return users[uid]


# ================= MENUS =================

def main_menu():
    return ReplyKeyboardMarkup(
        [
            ["💰 Deposit"],
            ["👤 My Profile", "🧑 Support"],
            ["📖 How to Use"],
            ["🔥 Thala Owner Services", "🏷️ Discount"]
        ],
        resize_keyboard=True
    )

def service_menu():
    return ReplyKeyboardMarkup(
        [
            ["🔥 Thala Skin", "👁️ Thala Hide ESP"],
            ["🔙 Back"]
        ],
        resize_keyboard=True
    )

def skin_menu():
    return ReplyKeyboardMarkup(
        [
            ["₹300 Full Season", "₹49 Testing"],
            ["🔙 Back"]
        ],
        resize_keyboard=True
    )

def esp_menu():
    return ReplyKeyboardMarkup(
        [
            ["₹400 Full Season", "₹65 Testing"],
            ["🔙 Back"]
        ],
        resize_keyboard=True
    )


# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    get_user(update.effective_user.id)
    await update.message.reply_text("Select option:", reply_markup=main_menu())


# ================= MAIN HANDLER =================

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    user = get_user(user_id)

    # BACK
    if text == "🔙 Back":
        await update.message.reply_text("Main Menu 👇", reply_markup=main_menu())

    # PROFILE
    elif text == "👤 My Profile":
        await update.message.reply_text(f"💰 Balance: ₹{user['balance']}")

    # SUPPORT
    elif text == "🧑 Support":
        await update.message.reply_text("Contact admin @yourusername")

    # 🔥 DEPOSIT (QR)
    elif text == "💰 Deposit":
        await context.bot.forward_message(
            chat_id=update.message.chat_id,
            from_chat_id=CHANNEL_ID,
            message_id=QR_MESSAGE_ID
        )

        await update.message.reply_text("💰 Payment karo aur UTR bhejo")

    # 🔥 UTR RECEIVED
    elif text.isdigit() and len(text) >= 10:
        pending[user_id] = {"utr": text}

        keyboard = [
            ["₹10", "₹20", "₹50"],
            ["₹100", "₹200", "₹500"]
        ]

        await update.message.reply_text(
            "💸 Kitna payment kiya?\nSelect karo ya amount likho:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )

    # 🔥 AMOUNT RECEIVE
    elif user_id in pending and (text.startswith("₹") or text.isdigit()):
        amount = int(text.replace("₹", ""))

        pending[user_id]["amount"] = amount
        utr = pending[user_id]["utr"]

        keyboard = [
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user_id}"),
                InlineKeyboardButton("❌ Decline", callback_data=f"decline_{user_id}")
            ]
        ]

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"💰 Payment Request\n\nUser: {user_id}\nUTR: {utr}\nAmount: ₹{amount}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        await update.message.reply_text("⏳ Payment verify ho raha hai...")

    # HOW TO USE
    elif text == "📖 How to Use":
        await context.bot.forward_message(update.message.chat_id, CHANNEL_ID, HOW_TO_USE_VIDEO_ID)

    # DISCOUNT
    elif text == "🏷️ Discount":
        await update.message.reply_text("🔥 Special Discount Available!")

    # SERVICES
    elif text == "🔥 Thala Owner Services":
        await update.message.reply_text("Select service:", reply_markup=service_menu())

    elif text == "🔥 Thala Skin":
        await update.message.reply_text("Select plan:", reply_markup=skin_menu())

    elif text == "👁️ Thala Hide ESP":
        await update.message.reply_text("Select plan:", reply_markup=esp_menu())

    # ================= BUY =================

    elif text == "₹300 Full Season":
        if user["balance"] >= 300:
            user["balance"] -= 300
            await update.message.reply_text(f"✅ Skin Full\nKey: {SKIN_FULL_KEY}\nBalance: ₹{user['balance']}")
            await context.bot.forward_message(update.message.chat_id, CHANNEL_ID, SKIN_FULL_FILE)
            await context.bot.forward_message(update.message.chat_id, CHANNEL_ID, COMMON_VIDEO_ID)
        else:
            await update.message.reply_text("❌ Balance kam hai")

    elif text == "₹49 Testing":
        if user["balance"] >= 49:
            user["balance"] -= 49
            await update.message.reply_text(f"✅ Skin Test\nKey: {SKIN_TEST_KEY}\nBalance: ₹{user['balance']}")
            await context.bot.forward_message(update.message.chat_id, CHANNEL_ID, SKIN_TEST_FILE)
        else:
            await update.message.reply_text("❌ Balance kam hai")

    elif text == "₹400 Full Season":
        if user["balance"] >= 400:
            user["balance"] -= 400
            await update.message.reply_text(f"✅ ESP Full\nKey: {ESP_FULL_KEY}\nBalance: ₹{user['balance']}")
            await context.bot.forward_message(update.message.chat_id, CHANNEL_ID, ESP_FULL_FILE)
            await context.bot.forward_message(update.message.chat_id, CHANNEL_ID, COMMON_VIDEO_ID)
        else:
            await update.message.reply_text("❌ Balance kam hai")

    elif text == "₹65 Testing":
        if user["balance"] >= 65:
            user["balance"] -= 65
            await update.message.reply_text(f"✅ ESP Test\nKey: {ESP_TEST_KEY}\nBalance: ₹{user['balance']}")
            await context.bot.forward_message(update.message.chat_id, CHANNEL_ID, ESP_TEST_FILE)
        else:
            await update.message.reply_text("❌ Balance kam hai")

    else:
        await update.message.reply_text("Option select karo 👇", reply_markup=main_menu())


# ================= ADMIN =================

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, user_id = query.data.split("_")
    user_id = int(user_id)

    user = get_user(user_id)

    if action == "approve":
        amount = pending[user_id]["amount"]
        user["balance"] += amount

        await context.bot.send_message(
            chat_id=user_id,
            text=f"✅ Payment Approved\nAmount: ₹{amount}\nBalance: ₹{user['balance']}"
        )

        del pending[user_id]
        await query.edit_message_text("✅ Approved")

    elif action == "decline":
        await context.bot.send_message(chat_id=user_id, text="❌ Payment Declined")
        await query.edit_message_text("❌ Declined")


# ================= RUN =================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle))
app.add_handler(CallbackQueryHandler(button))

print("FINAL BOT RUNNING...")
app.run_polling()