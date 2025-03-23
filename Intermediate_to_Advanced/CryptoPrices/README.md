# 📉 Crypto Price Notifier

A real-time cryptocurrency tracker and price alert system built using **Flask**, **Flask-SocketIO**, and **Vanilla JavaScript**. This application allows users to monitor live prices of cryptocurrencies and set custom notifications when a specific coin hits a user-defined price threshold.

With a clean and responsive user interface, automatic price updates, and background watchers, this project demonstrates real-time full-stack integration and effective asynchronous handling between the frontend and backend.

---

## 🚀 Features

- ✅ **Live cryptocurrency prices** fetched from the [CoinCap API](https://api.coincap.io)
- 🔔 **Real-time price alert notifications** using WebSocket communication
- 🔁 **Automatic price refresh** every 20 seconds for the latest market data
- 🧠 **Custom watchlist setup** with user-defined target prices
- 🌐 **Responsive web UI** built with clean and dynamic JavaScript
- 🧩 **Modular and reusable code structure** for easy maintainability and extension

---

## 🛠️ Technologies Used

- **Python 3** – Core backend language
- **Flask** – Lightweight Python web framework
- **Flask-SocketIO** – Real-time communication over WebSockets
- **HTML5 / CSS3** – Page structure and styling
- **Vanilla JavaScript** – Frontend logic and event handling
- **CoinCap Public API** – Source of real-time crypto data

---

## 📁 Project Structure

```
CryptoPrices/
├── static/
│   ├── js/
│   │   └── script.js
│   └── css/
│       └── style.css
├── templates/
│   └── index.html
├── app.py
├── crypto_notifier.py
└── README.md
```

---

## 📚 Installation & Running

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Setup

```bash
git clone https://github.com/Nemanja264/Python-Projects.git
cd Python-Projects/Intermediate_to_Advanced/CryptoPrices
pip install flask flask-socketio requests
```

### Run the App

```bash
python app.py
```

Open your browser at:

```
http://127.0.0.1:5555
```

---

## 📊 How It Works

- The **backend** fetches real-time prices from CoinCap and exposes them via an API endpoint.
- The **frontend** uses `fetch()` to retrieve prices and update the UI every 20 seconds.
- When a user sets a price limit, the backend spawns a **background thread** that watches the price.
- If the price crosses the threshold, the watcher sends a WebSocket message to the client.
- The frontend receives this message and **displays an alert notification**.

---

## 📅 License

This project is licensed under the [MIT License](LICENSE), allowing you to use, modify, and distribute it freely.

---

## 👥 Author

**Nemanja264**

🔗 GitHub: [Nemanja264](https://github.com/Nemanja264)

If you like this project, please consider giving it a ⭐, and feel free to contribute or report issues!

