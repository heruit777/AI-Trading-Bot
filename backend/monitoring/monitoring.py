from backend.redis_client import RedisClient
from backend.config import instrument_keys
import json

class Monitoring():
    '''
        To check if the trade hit SL or TP
    '''
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is not None:
            raise Exception("This is a singleton class. Use `get_instance()` to access the instance.")
        return super().__new__(cls)

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = Monitoring()
        return cls._instance

    # don't use the constructor to create the objects
    def __init__(self):
        self.redis_client = RedisClient.get_instance()
        self.running_trades = [] # Trades that are live
        self.pending_trades = [] # Trades that are still in pending status (not live yet)

    def subscribe_to_ticks(self):
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe('Reliance')

        for message in pubsub.listen():
            if message['type'] == 'message':
                self.process_tick_data(json.loads(message['data']))

    def process_tick_data(self, tick_data: dict):
        ltpc = tick_data['feeds'][instrument_keys['Reliance']]['ltpc']
        # print(f'From Monitoring Module: Reliance ltp: {ltpc['ltp']} and ltq: {ltpc['ltq']}')
        # logic to monitor pl of orders

    def monitor_trade(self, order: dict, sl_order: dict):
        # Will take two order
        print(f'Monitoring {order} and {sl_order}')
        
    