from requests import get
import time
import threading

URL = "https://api.coincap.io/v2/assets"

def get_all_data(URL):
    response = get(URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch data from {URL}")
        return None

def get_coin_info(URL, coin):
    return get(f"{URL}/{coin}").json()

def get_coin_price(URL, coin):
    return get_coin_info(URL, coin)['data']['priceUsd']

def get_all_coins_printable(URL):
    data = get_all_data(URL)

    if data and 'data' in data:
        result = ""
        for coin in data['data']:
            result += f"{coin['name']}: ${float(coin['priceUsd']):.4f}\n"
        return result
    else:
        print("No coin data found")

def print_all_coins(URL):
    print(get_all_coins_printable(URL))

def price_limit_notifier(coin_price, coin):
    print(f"{coin.capitalize()} has reached limit you set, current price: {float(coin_price):.6f}")

def multiple_price_watcher(URL, watch_list):
    threads=[]
    for coin, limit in watch_list:
        thread = run_in_background(price_limit_watcher, URL, coin, limit)
        threads.append(thread)

    return threads

def price_limit_watcher(URL, coin, price_limit, notifier=price_limit_notifier):
    while True:
        try:
            coin_price = get_coin_price(URL, coin)

            if coin_price is None:
                print(f"Error fetching price for {coin}. Retrying...")
                time.sleep(10)
                continue

            if float(coin_price) >= price_limit:
                break
            time.sleep(15)
        except Exception as e:
            print(f"[{coin}] Watcher crashed: {e}. Retrying in 15s...")
            time.sleep(20)

    notifier(coin_price, coin)
    return coin_price

def run_in_background(func, *args, **kwargs):
    thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    thread.start()
    return thread

def wait_for_threads(threads):
    for thread in threads:
        thread.join()

def coin_selector():
    coins=[]
    print("Input about which coins do you want to be notified and their price limits:")
    while True:
        coin = input("Coin: ").lower()
        price_limit = float(input("Price limit: "))
        coins.append((coin, price_limit))

        if input("\nDo you have more coins you want to be notified about?\nPress any key to continue, 'q' to quit\n").lower() == 'q':
            break

    return coins

def main():
    coins = coin_selector()
    for coin, price_limit in coins:
        print(f"{coin.capitalize()}, price limit: ${price_limit}")

    threads = multiple_price_watcher(URL, coins)
    threads.append(run_in_background(print_all_coins, URL))

    wait_for_threads(threads)

#main()