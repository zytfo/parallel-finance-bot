import requests
import re
import json


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


if __name__ == "__main__":
    print(get_prices())
