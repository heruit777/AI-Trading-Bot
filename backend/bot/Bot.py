import asyncio
import json
from backend.logger_config import logger
from backend.brokers.broker import Broker
from backend.strategies.strategy import TradingStrategy
from backend.monitoring.monitoring import Monitoring
from concurrent.futures import ThreadPoolExecutor
import backend.config as config
from backend.redis_client import RedisClient

class Bot():
    '''
        Main interaction point. This will utilize all the other classes
    '''
    def __init__(self, user_broker_map: dict[str, Broker], strategy: TradingStrategy, admin_broker: Broker):
        self.user_broker_map = user_broker_map
        self.strategy = strategy
        self.monitor = Monitoring.get_instance()
        self.redis_client = RedisClient.get_instance()
        self.admin_broker = admin_broker

    async def listen_for_trade_signal(self):
        pubsub = self.redis_client.pubsub()
        await pubsub.subscribe('trade_signal')

        async for message in pubsub.listen():
            if message['type'] == 'message':
                asyncio.create_task(self.execute_trade_for_all_users(json.loads(message['data'])))  # Schedule the trade execution asynchronously

    async def execute_trade_for_all_users(self, trade_signal: dict):
        '''
            It will subscribe to channel 'trade_signal' and will receive the trade order and execute that trade for all the user in the user_broker_map
        '''
        # Instead of asyncio.run(), directly await the async function
        logger.info('Executing trade for all the users')
        await asyncio.gather(*[broker.send_order(userId, trade_signal) for userId, broker in self.user_broker_map.items()])

        logger.info('Trade executed for all the users')

    async def helper(self):
        loop = asyncio.get_running_loop()
        executor = ThreadPoolExecutor(5)

        # await self.redis_client.delete('in_trade')

        await self.redis_client.hset(config.INSTRUMENT_PRICES_KEY, mapping={
            "Reliance": 0
        })
        
        await asyncio.gather(
            # loop.run_in_executor(executor, self.strategy.subscribe_to_ticks),
            # loop.run_in_executor(executor, self.monitor.subscribe_to_ticks),
            # loop.run_in_executor(executor, self.listen_for_trade_signal),
            self.admin_broker.demo_fetch_and_publish_ticks(),
            self.strategy.subscribe_to_ticks(),
            self.monitor.subscribe_to_ticks(),
            self.listen_for_trade_signal()
            # self.broker.fetch_and_publish_ticks()
        )

    def run(self):
        asyncio.create_task(self.helper())
        # Use asyncio.run only for starting the main helper function (entry point)
        # if not asyncio.get_event_loop().is_running():  # Only use asyncio.run if an event loop is not already 
        #     logger.info('Loop is running')
        #     asyncio.run(self.helper())
        # else:
        #     # If already running, directly call helper
        #     asyncio.create_task(self.helper())  # Schedule the helper to be run in the existing event loop
