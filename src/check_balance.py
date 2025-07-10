from binance.client import Client
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

client = Client(api_key, api_secret, testnet=True)

try:
    balances = client.futures_account_balance()
    for b in balances:
        if b["asset"].upper() == "USDT":
            print(f"✅ USDT Balance: {b['balance']}")
except Exception as e:
    print(f"❌ ERROR: {e}")
