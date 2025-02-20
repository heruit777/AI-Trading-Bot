import asyncio
import json
from backend.logger_config import logger
import backend.config as config
from backend.brokers.broker import Broker
from backend.strategies.strategy import TradingStrategy
from backend.monitoring.monitoring import Monitoring
from backend.risk_management.risk_management import Risk_Management
from concurrent.futures import ThreadPoolExecutor
import backend.config as config
from backend.strategies.strategy1 import RandomStrategy
from backend.strategies.llmstrategy import LLMStrategy
from backend.redis_client import RedisClient

class Bot():
    '''
        Main interaction point. This will utilize all the other classes
    '''
    def __init__(self, user_broker_map: dict[str, Broker], admin_broker: Broker):
        self.user_broker_map = user_broker_map
        self.strategy = RandomStrategy() # LLMStrategy(), to use it you may have
        self.monitor = Monitoring.get_instance()
        self.risk_manager = Risk_Management()
        self.redis_client = RedisClient.get_instance()
        self.admin_broker = admin_broker

    async def listen_for_trade_signal(self):
        pubsub = self.redis_client.pubsub()
        await pubsub.subscribe('trade_signal')

        async for message in pubsub.listen():
            if message['type'] == 'message':
                asyncio.create_task(self.execute_trade_for_all_users(json.loads(message['data'])))  # Schedule the trade execution asynchronously

    async def process_trade(self, userId: str, broker: Broker, trade_signal: dict):
        # do risk analysis and if it's valid then take the trade
        order = await self.risk_manager.analyze(userId, trade_signal)
        if order == 'MAX_TRADE_LIMIT_REACHED':
            if userId in config.user_connections:
                print(f'Removed user [{userId}] because {order}')
                await config.user_connections[userId].close()
                del config.user_connections[userId]

            return
        if order:
            # if config.IN_TRADE == False:
            #     config.IN_TRADE = True
            await broker.send_order(userId, order)
        else:
            logger.info(f'Cannot execute this trade for User Id: [{userId}], SL is too big')

    async def execute_trade_for_all_users(self, trade_signal: dict):
        '''
            It will subscribe to channel 'trade_signal' and will receive the trade order and execute that trade for all the user in the user_broker_map
        '''
        if config.IN_TRADE:
            logger.info('One trade is already running, so cannot execute another trade')
            return 
        
        config.IN_TRADE = True
        tasks = [self.process_trade(userId, broker, trade_signal) for userId, broker in self.user_broker_map.items()]
        await asyncio.gather(*tasks)
        logger.info('Finish executing trades for all the eligible users')
        
        # Instead of asyncio.run(), directly await the async function
        # logger.info('Executing trade for all the users')
        # await asyncio.gather(*[broker.send_order(userId, trade_signal) for userId, broker in self.user_broker_map.items()])

        # logger.info('Trade executed for all the users')
        # logger.info(f'History: {self.monitor.history}')

    async def helper(self):
        loop = asyncio.get_running_loop()
        executor = ThreadPoolExecutor(5)

        # await self.redis_client.delete('in_trade')
        # So that broker has access to market prices
        await self.redis_client.hset(config.INSTRUMENT_PRICES_KEY, mapping={
            "Reliance": 0
        })
        
        await asyncio.gather(
            # loop.run_in_executor(executor, self.strategy.subscribe_to_ticks),
            # loop.run_in_executor(executor, self.monitor.subscribe_to_ticks),
            # loop.run_in_executor(executor, self.listen_for_trade_signal),
            self.admin_broker.demo_fetch_and_publish_ticks(),
            # self.admin_broker.fetch_and_publish_ticks(),
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
