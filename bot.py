import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_1 = "t.me"
CHANNEL_2 = "@YOUR_TOOLS_CHANNEL"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔒 Main Channel", url="https://t.me/SanchezServices")],
        [InlineKeyboardButton("🔒 Vouches/Confos", url="https://t.me/SanchezVouchesandConfos")],
        [InlineKeyboardButton("✅ Check Access", callback_data="check")]
    ]

    await update.message.reply_text(
        "👋 Welcome to Sanchez's Gateway Portal!\n\n"
        "Join the required channels below, then press **Check Access**.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


async def check_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    try:
        member1 = await context.bot.get_chat_member(CHANNEL_1, user_id)
        member2 = await context.bot.get_chat_member(CHANNEL_2, user_id)

        valid_statuses = ["member", "administrator", "creator"]

        if member1.status in valid_statuses and member2.status in valid_statuses:
            await query.edit_message_text(
                "✅ Access verified!\n\n"
                "You have joined all required channels."
            )
        else:
            await query.answer(
                "❌ You need to join both channels first.",
                show_alert=True
            )

    except Exception:
        await query.answer(
            "⚠️ I couldn't check your membership. Make sure the bot is an admin in both channels.",
            show_alert=True
        )


async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    from telegram.ext import CallbackQueryHandler
    app.add_handler(CallbackQueryHandler(check_access, pattern="^check$"))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
