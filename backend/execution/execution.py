from backend.brokers.broker import Broker

class Execution():
    '''
        Send the order to the broker
    '''
    def __init__(self, broker: Broker):
        self.broker = broker

    def send_market_order(self, trade: dict):
        # use broker to send a market order
        self.broker.send_market_order(trade)

    def send_limit_order(self, trade: dict):
        # use broker to send a limit order
        pass

    def send_stop_loss_market_order(self, trade: dict):
        # use broker to send a stop loss market order
        pass

