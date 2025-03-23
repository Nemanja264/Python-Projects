from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_socketio import SocketIO, emit 
from crypto_notifier import run_in_background, price_limit_watcher, get_all_data, URL, get_all_coins_printable

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def socket_notifier(coin_price, coin):
    socketio.emit('limit_reached', {'coin': coin, 'price': float(coin_price)})

@app.route('/api/prices')
def get_prices():
    data = get_all_data(URL)

    if data and 'data' in data:
        coins_data = [{"name": coin['name'], "priceUsd": coin['priceUsd']} for coin in data['data']]
        return jsonify(coins_data)

    return jsonify([])

@app.route('/api/price_watcher/<coin_name>/<price_limit>')
def watch_price_limit(coin_name, price_limit):
    price_limit = float(price_limit)

    run_in_background(price_limit_watcher, URL, coin_name, price_limit, socket_notifier)

    return jsonify({'status': f'Watcher started for {coin_name} with limit {price_limit}'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5555, debug=True, use_reloader=False)
