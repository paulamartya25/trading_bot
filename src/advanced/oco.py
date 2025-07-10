def place_oco_order(client, symbol, side, quantity, price, stop_price):
    try:
        return client.futures_create_order(
            symbol=symbol,
            side=side,
            type="STOP_MARKET",
            stopPrice=str(stop_price),
            closePosition=True
        )
    except Exception as e:
        raise RuntimeError(f"❌ OCO order failed: {e}")
