from api_client import APIClient
from trade_manager import TradeManager

if __name__ == "__main__":

    # get api secret.
    with open("./.api_secret") as secret_file:
        api_secret = secret_file.readline()

    # subscribe to channels.
    symbol = "BTC-USD"
    client = APIClient(api_secret)
    client.subscribe_trading()
    client.subscribe_ticker(symbol)

    # bot does simple market making.
    trade_manager = TradeManager(client, symbol)
    trade_manager.trade(max_num_orders=2, max_num_days=1)
