from backend.strategies.strategy import TradingStrategy
from backend.redis_client import RedisClient
from backend.brokers.broker import Broker
from backend.config import instrument_keys
from backend.risk_management.risk_management import Risk_Management
import json
import random

class MovingAverageStrategy(TradingStrategy):

    def __init__(self, broker: Broker):
        self.redis_client = RedisClient.get_instance()
        self.risk_manager = Risk_Management(broker)

    def subscribe_to_ticks(self):
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe('Reliance')

        for message in pubsub.listen():
            if message['type'] == 'message':
                self.process_tick_data(json.loads(message['data']))

    def core_logic(self, tick_data: dict):
        # logic here
        num = random.randint(0, 2) # 0: buy, 1: sell, 2: hold
        price = tick_data['feeds'][instrument_keys['Reliance']]['ltpc']['ltp']
        sl = 1 # 1 Rs 
        if num == 0 :
            return {'type': 'buy', 'price': price, 'sl': sl, 'instrument_token': instrument_keys['Reliance']}
        elif num == 1:
            return {'type': 'sell', 'price': price, 'sl': sl, 'instrument_token': instrument_keys['Reliance']}
        else:
            return {'type': 'hold', 'instrument_token': instrument_keys['Reliance']}
        

    def process_tick_data(self, tick_data: dict):
        ltpc = tick_data['feeds'][instrument_keys['Reliance']]['ltpc']
        print(f'From Moving Average Strategy Module: Reliance ltp: {ltpc['ltp']} and ltq: {ltpc['ltq']}')
        signal = self.core_logic(tick_data)
        if signal['type'] == 'hold':
            print('No Trade')
        else:
            print(f'Trade found: {signal}')
            
            self.risk_manager.validate_signal(signal)
        

    