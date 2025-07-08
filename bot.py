# bot.py

from binance.client import Client
from binance.enums import *
from dotenv import load_dotenv
import os

class TradingBot:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("API_KEY")
        api_secret = os.getenv("API_SECRET")

        if not api_key or not api_secret:
            raise Exception("❌ API_KEY or API_SECRET missing in .env")

        self.client = Client(api_key, api_secret, testnet=True)

    def get_balance(self):
        try:
            account_info = self.client.futures_account()
            balance = float(account_info["totalWalletBalance"])
            return balance
        except Exception as e:
            print("❌ Error fetching balance:", e)
            return None

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            params = {
                "symbol": symbol.upper(),
                "side": SIDE_BUY if side.upper() == "BUY" else SIDE_SELL,
                "type": ORDER_TYPE_MARKET if order_type.upper() == "MARKET" else ORDER_TYPE_LIMIT,
                "quantity": quantity
            }

            if order_type.upper() == "LIMIT":
                if not price:
                    raise ValueError("Price is required for limit orders.")
                params["price"] = str(price)
                params["timeInForce"] = TIME_IN_FORCE_GTC

            order = self.client.futures_create_order(**params)
            print("✅ Order placed successfully!")
            return order

        except Exception as e:
            print("❌ Order failed:", e)
            return None
