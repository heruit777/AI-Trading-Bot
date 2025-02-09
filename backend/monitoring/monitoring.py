from backend.redis_client import RedisClient
import backend.config as config
from backend.logger_config import logger
import json
from typing import Literal

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
        self.orders = [] # Trades that are live
        self.cover_orders = [] # Trades that are still in pending status (not live yet)
        self.history: dict[str, list] = {}
        self.is_monitor = False

    async def subscribe_to_ticks(self):
        pubsub = self.redis_client.pubsub()
        await pubsub.subscribe('Reliance')

        async for message in pubsub.listen():
            if message['type'] == 'message':
                self.process_tick_data(json.loads(message['data']))

    def update_history(self, userId: str):
        # remove order and cover order and place it in history 
        order = self.orders.pop(0) # This can be an issue in future.
        cover_order = self.cover_orders.pop(0)
        if userId in self.history:
            self.history[userId].append({'order': order, 'cover_order': cover_order})
        else:
            self.history[userId] = [{'order': order, 'cover_order': cover_order}]

    def process_tick_data(self, tick_data: dict):
        ltpc = tick_data['feeds'][config.instrument_keys['Reliance']]['ltpc']['ltp']
        # logger.info(f'From Monitoring Module: Reliance ltp: {ltpc['ltp']} and ltq: {ltpc['ltq']}')
        # logic to monitor pl of orders
        for trade in self.cover_orders:
            if trade['transaction_type'] == 'buy':
                # logger.info(f'{ltpc} {trade['order']['trigger_price']}')
                if ltpc <= trade['order']['trigger_price']:
                    userId, orderId = trade['order']['user_id'], trade['order']['order_id']
                    logger.info(f'SL trigger for Order Id: [{orderId}], User Id: [{userId}]')
                    self.update_history(userId)
            else:
                if ltpc >= trade['order']['trigger_price']:
                    userId, orderId = trade['order']['user_id'], trade['order']['order_id']
                    logger.info(f'SL trigger for Order Id: [{orderId}], User Id: [{userId}]')
                    self.update_history(userId)

        # if no trades are being monitored then you can update the redis in_trade variable to false
        logger.info(f'orders: {self.orders} and cover_orders: {self.cover_orders}')
        if self.is_monitor and not self.orders and not self.cover_orders:
            config.IN_TRADE = False
            self.is_monitor = False

    def monitor_trade(self, transaction_type: Literal['buy', 'sell'],order: dict, sl_order: dict):
        # Will take two order
        self.is_monitor = True
        logger.info(f'Monitoring {order} and {sl_order}')
        self.orders.append({'transaction_type': transaction_type, 'order': order})
        self.cover_orders.append({'transaction_type': transaction_type, 'order': sl_order})

        
    