import time

def place_twap_order(client, symbol, side, total_quantity, intervals, delay):
    try:
        qty_per_order = round(total_quantity / intervals, 6)

        for i in range(intervals):
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=qty_per_order
            )
            print(f"✅ TWAP Order {i+1}/{intervals} executed: {order['orderId']}")
            time.sleep(delay)

        return True
    except Exception as e:
        print(f"❌ TWAP order failed: {e}")
        return False
