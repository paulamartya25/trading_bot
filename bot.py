import os
import logging
from dotenv import load_dotenv
from binance.client import Client
from binance.enums import *

# Load API credentials
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Setup logging
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

class TradingBot:
    def __init__(self, testnet=True):
        self.client = Client(API_KEY, API_SECRET)
        if testnet:
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        logging.info("Initialized Binance Testnet client")

    def get_balance(self, asset="USDT"):
        try:
            balances = self.client.futures_account_balance()
            for b in balances:
                if b["asset"] == asset:
                    logging.info(f"Fetched {asset} balance: {b['balance']}")
                    return float(b["balance"])
            return 0.0
        except Exception as e:
            logging.error(f"Balance fetch failed: {e}")
            return 0.0

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        try:
            symbol = symbol.upper()
            side = SIDE_BUY if side.upper() == "BUY" else SIDE_SELL
            order_type = order_type.upper()

            order_params = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "quantity": quantity
            }

            if order_type == "LIMIT":
                order_params["price"] = str(price)
                order_params["timeInForce"] = TIME_IN_FORCE_GTC

            elif order_type == "STOP_LIMIT":
                order_params["stopPrice"] = str(stop_price)
                order_params["price"] = str(price)
                order_params["timeInForce"] = TIME_IN_FORCE_GTC

            logging.info(f"Placing {order_type} order: {order_params}")
            order = self.client.futures_create_order(**order_params)
            logging.info(f"✅ Order placed successfully: {order}")
            return order

        except Exception as e:
            logging.error(f"❌ Order failed: {e}")
            return None
