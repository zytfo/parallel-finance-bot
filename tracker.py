import requests
import re
import json
from datetime import datetime


def get_prices():
    assets_page = 'https://analytics.parallel.fi/api/assets/prices/'
    page_text = requests.get(assets_page).text
    expr = 'window.pricingData = (.*);</script><div id="root"></div><script src="/bundle.js"'
    result = re.search(expr, page_text)
    pricing_data = json.loads(result.group(1))

    data = {}
    coins = list(pricing_data.keys())

    for coin in coins:
        try:
            data[coin] = {
                "coin": coin,
                "price": pricing_data[coin][-1]['close'],
                "previous_price": pricing_data[coin][-2]['close']
            }
        except IndexError:
            continue
    return data


def get_message(is_telegram):
    utc_time = datetime.utcnow()
    current_time = utc_time.strftime('%Y-%m-%d %H:%M:%S')
    message = ""
    crypto_data = get_prices()
    emoji = "➡️"
    tvl_url = "https://analytics.parallel.fi/api/amm/tvl"
    req = requests.get(url=tvl_url)
    tvl_data = req.json()

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
                       f"*Price:* ${price:,.3f}\n" \
                       f"*Day Change:* {emoji} {change_day:.2f}%\n\n"
        else:
            message += f"**Coin:** {coin}\n" \
                       f"**Price:** ${price:,.3f}\n" \
                       f"**Day Change:** {emoji} {change_day:.2f}%\n\n"

    # message += f"*TVL*: ${tvl_data['val']:,.2f}\n\n"
    message += f"_Last updated:_ _{current_time}_ _UTC_\n"
    return message
