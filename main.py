from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import BadRequest
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)
from tracker import get_message
import config


FIRST = range(1)


def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("🔄 Update", callback_data=str(FIRST)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text=get_message(is_telegram=True), parse_mode="Markdown", reply_markup=reply_markup)


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
            text=get_message(is_telegram=True), parse_mode="Markdown", reply_markup=reply_markup
        )
    except BadRequest:
        pass


def main() -> None:
    updater = Updater(token=config.BOT_TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('update', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(refresh))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
