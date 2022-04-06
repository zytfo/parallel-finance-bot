from telegram.ext import Updater
from telegram.ext import CommandHandler
from tracker import get_prices
import config

telegram_bot_token = config.BOT_TOKEN

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    chat_id = update.effective_chat.id
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
    context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")


dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("prices", start))
updater.start_polling()
