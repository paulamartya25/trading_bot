def place_market_order(client, symbol, side, quantity):
    try:
        return client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )
    except Exception as e:
        raise RuntimeError(f"❌ Market order failed: {e}")
