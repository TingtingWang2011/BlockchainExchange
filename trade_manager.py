import datetime as dt
import json
import time
import uuid


class TradeManager:
    def __init__(self, client, symbol):
        """ Create a trade manager to do simple market making.

        Parameters
        ----------
        client: BCExchangeAPIClient
            client to collect to Blockchain Exchange https://exchange.blockchain.com
        symbol: str
            Blockchain Exchange instrument symbol
        """
        self.client = client
        self.symbol = symbol
        self.last_trade_price = None
        self.order_status = dict()

    def _parse_response(self, resp):
        """ Parse response received from the API

        Parameters
        ----------
        resp: str
            response received from the API
        """
        if not resp:
            return

        json_resp = json.loads(resp)
        print(json_resp)

        if json_resp.get("event") == "subscribed":
            return

        if json_resp["channel"] == "ticker":
            self.last_trade_price = json_resp.get("last_trade_price")
        elif json_resp["channel"] == "trading":
            if json_resp["event"] == "snapshot":
                for order in json_resp["orders"]:
                    self.order_status[order["orderID"]] = order["ordStatus"]

    def trade(self, max_num_orders, max_num_days):
        num_orders = 0
        sleep_time = 5
        end_dt = dt.datetime.now() + dt.timedelta(days=max_num_days)

        # loop till end date.
        print(f"start trading")
        while dt.datetime.now() < end_dt:
            resp = self.client.receive()
            self._parse_response(resp)

            # create orders.
            if num_orders < max_num_orders and self.last_trade_price is not None:
                # buy with slightly lower price.
                price = self.last_trade_price * 0.99
                quantity = 1.0 / price
                cl_order_id = str(uuid.uuid1())[:20]
                print(f"creating buy order at price {price} with quantity {quantity}")
                self.client.create_order(
                    order_id=cl_order_id,
                    symbol=self.symbol,
                    order_type="limit",
                    time_in_force="GTC",
                    side="buy",
                    quantity=quantity,
                    price=price,
                )

                # sell with slightly higher price.
                price = self.last_trade_price * 1.01
                quantity = 1.0 / price
                cl_order_id = str(uuid.uuid1())[:20]
                print(f"creating sell order at price {price} with quantity {quantity}")
                self.client.create_order(
                    order_id=cl_order_id,
                    symbol=self.symbol,
                    order_type="limit",
                    time_in_force="GTC",
                    side="sell",
                    quantity=quantity,
                    price=price,
                )

                num_orders += 2
                time.sleep(sleep_time)

        # cancel all live orders.
        live_orders = [
            order_id
            for order_id, status in self.order_status.items()
            if status in ["pending", "open"]
        ]
        if len(live_orders) > 0:
            print(f"cancelling {len(live_orders)} orders")
            self.client.cancel_all_orders(live_orders)

        # close connection.
        self.client.close()
        print(f"end trading")
