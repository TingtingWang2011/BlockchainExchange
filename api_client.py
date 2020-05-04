import json

from websocket import create_connection


class APIClient:
    def __init__(self, api_secret):
        """ Create a Blockchain Exchange API client to handle I/O.

        Parameters
        ----------
        api_secret: str
            Blockchain Exchange API secret, see https://exchange.blockchain.com/api/#to-get-started
        """
        options = {"origin": "https://exchange.blockchain.com"}
        url = "wss://ws.prod.blockchain.info/mercury-gateway/v1/ws"
        self.ws = create_connection(url, **options)
        msg = {"token": api_secret, "action": "subscribe", "channel": "auth"}
        self.ws.send(json.dumps(msg))

    def subscribe_heart_beat(self):
        msg = {"action": "subscribe", "channel": "heartbeat"}
        self.ws.send(json.dumps(msg))

    def subscribe_l2_lob(self, symbol):
        msg = {
            "action": "subscribe",
            "channel": "l2",
            "symbol": symbol,
        }
        self.ws.send(json.dumps(msg))

    def subscribe_l3_lob(self, symbol):
        msg = {"action": "subscribe", "channel": "l3", "symbol": symbol}
        self.ws.send(json.dumps(msg))

    def subscribe_prices(self, symbol, granularity):
        if granularity not in [60, 300, 900, 3600, 21600, 86400]:
            raise ValueError(f"granularity {granularity} not supported")

        msg = {
            "action": "subscribe",
            "channel": "prices",
            "symbol": symbol,
            "granularity": granularity,
        }
        self.ws.send(json.dumps(msg))

    def subscribe_symbols(self):
        msg = {"action": "subscribe", "channel": "symbols"}
        self.ws.send(json.dumps(msg))

    def subscribe_ticker(self, symbol):
        msg = {"action": "subscribe", "channel": "ticker", "symbol": symbol}
        self.ws.send(json.dumps(msg))

    def subscribe_trades(self, symbol):
        msg = {"action": "subscribe", "channel": "trades", "symbol": symbol}
        self.ws.send(json.dumps(msg))

    def subscribe_trading(self):
        msg = {
            "action": "subscribe",
            "channel": "trading",
        }
        self.ws.send(json.dumps(msg))

    def subscribe_balances(self):
        msg = {"action": "subscribe", "channel": "balances"}
        self.ws.send(json.dumps(msg))

    def create_order(self, order_id, symbol, order_type, time_in_force, side, quantity, price):
        if order_type not in ["limit", "market", "stop", "stopLimit"]:
            raise ValueError(f"order_type {order_type} not recognised")
        if time_in_force not in ["GTC", "GTD", "FOK", "IOC"]:
            raise ValueError(f"time_in_force {time_in_force} not recognised")
        if side not in ["buy", "sell"]:
            raise ValueError(f"side {side} not recognised")
        if quantity < 0:
            raise ValueError(f"Invalid quantity: {quantity}")
        if price < 0:
            raise ValueError(f"Invalid price: {price}")

        msg = {
            "action": "NewOrderSingle",
            "channel": "trading",
            "clOrdID": order_id,
            "symbol": symbol,
            "ordType": order_type,
            "timeInForce": time_in_force,
            "side": side,
            "orderQty": quantity,
            "price": price,
            "execInst": "ALO",
        }

        self.ws.send(json.dumps(msg))
        print(json.dumps(msg))

    def cancel_order(self, order_id):
        msg = {"action": "CancelOrderRequest", "channel": "trading", "orderID": order_id}
        self.ws.send(json.dumps(msg))

    def cancel_all_orders(self, order_ids):
        for order_id in order_ids:
            self.cancel_order(order_id)

    def receive(self):
        return self.ws.recv()

    def close(self):
        self.ws.close()
