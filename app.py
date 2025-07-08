# app.py

from flask import Flask, render_template, request, redirect, flash
from bot import TradingBot

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for flashing messages
bot = TradingBot()

@app.route("/", methods=["GET", "POST"])
def index():
    balance = bot.get_balance()
    
    if request.method == "POST":
        symbol = request.form.get("symbol", "BTCUSDT").upper()
        side = request.form.get("side", "BUY").upper()
        order_type = request.form.get("order_type", "MARKET").upper()
        quantity = float(request.form.get("quantity", 0))
        price = request.form.get("price")
        price = float(price) if price else None

        result = bot.place_order(symbol, side, order_type, quantity, price)

        if result:
            flash("✅ Order placed successfully!", "success")
        else:
            flash("❌ Order failed. Check console.", "danger")

        return redirect("/")

    return render_template("index.html", balance=balance)
if __name__ == "__main__":
    app.run(debug=True)
