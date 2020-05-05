# BlockchainExchange
This repo implements [Blockchain Exchange API](https://exchange.blockchain.com/api/#introduction).
You will need to obtain an API secret by following instructions [here](https://exchange.blockchain.com/api/#to-get-started) and add to `./.api_secret`. 

Command to run the code:
```
python runner.py
```

Features implemented in this demo code:
* Connect to the exchange using websocket API.
* Subscribe to the following channels: e.g. heart_beat, l2_lob, l3_lob, prices, symbols, ticker, trades, trading, balances. 
* Create and cancel orders.
* Market making bot that creates limit orders based on the last traded prices and cancels live orders after timeout.

Dependencies:
* websocket
* websocket-client

