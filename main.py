from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import BadRequest
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)
from tracker import get_prices
from datetime import datetime
import config


FIRST = range(1)


def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("🔄 Update", callback_data=str(FIRST)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text=get_message(), parse_mode="Markdown", reply_markup=reply_markup)


def refresh(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("🔄 Update", callback_data=str(FIRST)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        query.edit_message_text(
            text=get_message(), parse_mode="Markdown", reply_markup=reply_markup
        )
    except BadRequest:
        pass


def get_message():
    utc_time = datetime.utcnow()
    current_time = utc_time.strftime('%Y-%m-%d %H:%M:%S')
    message = ""
    crypto_data = get_prices()
    emoji = "➡️"
    for i in crypto_data:
        coin = crypto_data[i]["coin"]
        price = crypto_data[i]["price"]
        previous_day_price = crypto_data[i]["previous_price"]
        change_day = (price - previous_day_price) / previous_day_price * 100
        if change_day > 0:
            emoji = "🚀"
        elif change_day < 0:
            emoji = "🔻️"
        message += f"*Coin:* {coin}\n" \
                   f"*Price:* ${price:,.2f}\n" \
                   f"*Day Change:* {emoji}{change_day:.2f}%\n\n"

    message += f"_Last updated:_ _{current_time}_ _UTC_\n"
    return message


def main() -> None:
    updater = Updater(token=config.BOT_TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('update', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(refresh))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
