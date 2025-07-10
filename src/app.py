from dotenv import load_dotenv
import os
from flask import Flask, render_template, request, redirect, flash
from bot import TradingBot

load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"

bot = TradingBot()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        symbol = request.form.get("symbol", "BTCUSDT").upper()
        side = request.form.get("side").upper()
        order_type = request.form.get("order_type").upper()
        quantity = float(request.form.get("quantity") or 0)
        price = request.form.get("price")
        stop_price = request.form.get("stop_price")

        price = float(price) if price else None
        stop_price = float(stop_price) if stop_price else None

        result = bot.place_order(symbol, side, order_type, quantity, price, stop_price)

        if result:
            flash("✅ Order placed successfully!", "success")
        else:
            flash("❌ Failed to place order. Check logs or values.", "danger")

    balance = bot.get_balance()
    return render_template("index.html", balance=balance)

if __name__ == "__main__":
    print("✅ Flask app starting...")
    app.run(debug=True)
