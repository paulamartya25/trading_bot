def place_limit_order(client, symbol, side, quantity, price):
    try:
        return client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=str(price)
        )
    except Exception as e:
        raise RuntimeError(f"❌ Limit order failed: {e}")
