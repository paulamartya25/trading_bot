import os
import logging
from dotenv import load_dotenv
from binance.client import Client
from binance.enums import *

# Load environment variables
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
        self.client = Client(API_KEY, API_SECRET, testnet=testnet)
        logging.info("✅ Initialized Binance Testnet client")

    def get_balance(self, asset="USDT"):
        try:
            balances = self.client.futures_account_balance()
            for b in balances:
                if b["asset"].upper() == asset.upper():
                    logging.info(f"✅ Fetched {asset} balance: {b['balance']}")
                    return float(b["balance"])
            logging.warning(f"⚠️ Asset {asset} not found in balance list.")
            return 0.0
        except Exception as e:
            logging.error(f"❌ Balance fetch failed: {e}")
            return 0.0

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        try:
            symbol = symbol.upper()
            side_enum = SIDE_BUY if side.upper() == "BUY" else SIDE_SELL
            order_type = order_type.upper()

            order_params = {
                "symbol": symbol,
                "side": side_enum,
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

            elif order_type == "MARKET":
                pass  # MARKET order only needs symbol, side, quantity

            else:
                logging.error(f"❌ Unsupported order type: {order_type}")
                return None

            logging.info(f"📦 Placing order: {order_params}")
            order = self.client.futures_create_order(**order_params)
            logging.info(f"✅ Order placed: {order}")
            return order

        except Exception as e:
            logging.error(f"❌ Order placement failed: {e}")
            return None
