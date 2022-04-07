import requests
import re
import json
from datetime import datetime


def get_prices():
    hko_page = 'https://analytics.parallel.fi/kusama/amm/HKO'
    page_text = requests.get(hko_page).text
    expr = 'window.pricingData = (.*);</script><div id="root"></div><script src="/bundle.js"'
    result = re.search(expr, page_text)
    pricing_data = json.loads(result.group(1))

    data = {}
    coins = list(pricing_data.keys())

    try:
        for coin in coins:
            data[coin] = {
                "coin": coin,
                "price": pricing_data[coin][-1]['close'],
                "previous_price": pricing_data[coin][-2]['close']
            }
    except IndexError:
        pass

    return data


def get_message(is_telegram):
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
            emoji = "🟩"
        elif change_day < 0:
            emoji = "🟥"
        if is_telegram:
            message += f"*Coin:* {coin}\n" \
                       f"*Price:* ${price:,.2f}\n" \
                       f"*Day Change:* {emoji} {change_day:.2f}%\n\n"
        else:
            message += f"**Coin:** {coin}\n" \
                       f"**Price:** ${price:,.2f}\n" \
                       f"**Day Change:** {emoji} {change_day:.2f}%\n\n"

    message += f"_Last updated:_ _{current_time}_ _UTC_\n"
    return message
