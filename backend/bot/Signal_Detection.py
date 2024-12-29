from brokers.broker import Broker
from strategies.strategy import TradingStrategy

class Signal_Detection():
    '''
        This will take data coming from the websocket and use a trading strategy to generate signal
    '''
    def __init__(self, broker: Broker, strategy: TradingStrategy):
        self.broker = broker
        self.strategy = strategy

    def find(self):
        # fetch tick by tick data from websocket and pass it to strategy
        self.broker.fetch_market_data(self.strategy.process_tick_data)
        # pass

