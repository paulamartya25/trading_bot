# main.py

from bot import TradingBot

bot = TradingBot()

# Show balance
balance = bot.get_balance()
if balance:
    print(f"💰 Your Futures Wallet Balance: {balance} USDT")

# Place an order
while True:
    symbol = input("Enter symbol (default BTCUSDT): ") or "BTCUSDT"
    side = input("Buy or Sell [buy/sell]: ").upper()
    order_type = input("Market or Limit [market/limit]: ").upper()
    quantity = float(input("Enter quantity: "))

    price = None
    if order_type == "LIMIT":
        price = float(input("Enter limit price: "))

    bot.place_order(symbol, side, order_type, quantity, price)

    again = input("Place another order? [y/n]: ")
    if again.lower() != 'y':
        break
