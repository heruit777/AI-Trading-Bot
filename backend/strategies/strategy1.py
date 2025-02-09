from backend.strategies.strategy import TradingStrategy
from backend.redis_client import RedisClient
import backend.config as config
from backend.logger_config import logger
from backend.risk_management.risk_management import Risk_Management
import json
import asyncio
import random

class MovingAverageStrategy(TradingStrategy):

    def __init__(self):
        self.redis_client = RedisClient.get_instance()
        self.risk_manager = Risk_Management(balance=config.BALANCE)

    async def subscribe_to_ticks(self):
        pubsub = self.redis_client.pubsub()
        await pubsub.subscribe('Reliance')

        async for message in pubsub.listen():
            if message['type'] == 'message':
                asyncio.create_task(self.process_tick_data(json.loads(message['data'])))

    def core_logic(self, tick_data: dict):
        # logic here
        num = random.randint(0, 2) # 0: buy, 1: sell, 2: hold
        price = tick_data['feeds'][config.instrument_keys['Reliance']]['ltpc']['ltp']
        sl = 1 # 1 Rs 
        if num == 0 :
            return {'type': 'buy', 'price': price, 'sl': sl, 'instrument_token': config.instrument_keys['Reliance']}
        elif num == 1:
            return {'type': 'sell', 'price': price, 'sl': sl, 'instrument_token': config.instrument_keys['Reliance']}
        else:
            return {'type': 'hold', 'instrument_token': config.instrument_keys['Reliance']}
        

    async def process_tick_data(self, tick_data: dict):
        ltpc = tick_data['feeds'][config.instrument_keys['Reliance']]['ltpc']
        logger.info(f'From Moving Average Strategy Module: Reliance ltp: {ltpc['ltp']} and ltq: {ltpc['ltq']}')
        signal = self.core_logic(tick_data)
        if signal['type'] == 'hold':
            logger.info('No Trade')
        else:
            logger.info(f'Trade found: {signal}')
            
            await self.risk_manager.validate_signal(signal)
        

    