from requests import get
import re

BASE_URL = "https://api.freecurrencyapi.com/v1/latest"

params = {
    "apikey": "fca_live_APiD8S2i9E05bwmjG11A4ij4SaEfQeqVgZv6MqPn",
    "base_currency": "",
    "currencies": ""
}

def get_currencies(url, params):
    response = get(url, params=params)
    data = response.json()
    return data['data']

def pick_base_currency():
    return input("Choose base currency: ").upper()

def pick_currencies():
    currencies = []
    print("Which currencies you need?")
    while True:
        currency = input("'Q' to quit: ").upper()
        if currency == 'Q':
            break

        currencies.append(currency)

    return currencies

def is_valid_number(value):
    return bool(re.fullmatch(r'\d+(\.\d+)?', value))

def pick_amount():
    while True:
        amount = input("Input amount you want to convert: ")
        if is_valid_number(amount):
            return float(amount)

        print("Invalid input, input must be a number")

def convert(amount, currency):
    return amount*currency

def display_conversions(amount, base_currency, currencies, data):
    for currency in currencies:
        converted_amount = convert(amount, data[currency])
        print(f"Conversion rate: {base_currency} -> {data[currency]:.2f} {currency}")
        print(f"${amount} {base_currency} = {converted_amount:.2f} {currency}\n")

def main():
    base_currency = pick_base_currency()
    params['base_currency'] = base_currency

    amount = pick_amount()

    currencies = pick_currencies()
    params['currencies'] = ','.join(currencies)

    data = get_currencies(BASE_URL, params)
    print(data)

    display_conversions(amount, base_currency, currencies, data)

main()