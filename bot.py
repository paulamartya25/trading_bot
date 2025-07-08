import os
import logging
from dotenv import load_dotenv
from binance.client import Client
from binance.enums import *

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Configure logging
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
            self.client.FUTURES_WEBSOCKET_URL = 'wss://stream.binancefuture.com/ws'
        logging.info("Initialized Binance Futures Testnet Client.")

    def get_balance(self, asset="USDT"):
        try:
            balance_info = self.client.futures_account_balance()
            for asset_info in balance_info:
                if asset_info["asset"] == asset:
                    logging.info(f"Retrieved balance: {asset_info['balance']} {asset}")
                    return float(asset_info["balance"])
            logging.warning(f"Asset {asset} not found in balance.")
            return 0.0
        except Exception as e:
            logging.error(f"Failed to fetch balance: {e}")
            return 0.0

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        try:
            symbol = symbol.upper()
            side = SIDE_BUY if side.upper() == "BUY" else SIDE_SELL
            order_type = order_type.upper()

            params = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "quantity": quantity
            }

            if order_type == "LIMIT":
                if not price:
                    raise ValueError("Limit price required for LIMIT order.")
                params["price"] = str(price)
                params["timeInForce"] = TIME_IN_FORCE_GTC

            elif order_type == "STOP_LIMIT":
                if not price or not stop_price:
                    raise ValueError("Both stop price and limit price required for STOP_LIMIT order.")
                params["stopPrice"] = str(stop_price)
                params["price"] = str(price)
                params["timeInForce"] = TIME_IN_FORCE_GTC

            elif order_type == "MARKET":
                pass  # No extra params needed

            logging.info(f"Placing {order_type} order: {params}")
            order = self.client.futures_create_order(**params)
            logging.info(f"✅ Order successful: {order}")
            return order

        except Exception as e:
            logging.error(f"❌ Order failed: {e}")
            return None
