import backend.config as config
from backend.redis_client import RedisClient
from backend.monitoring.monitoring import Monitoring
from backend.logger_config import logger
import json
import asyncio

class Risk_Management():
    '''
        It take signal and check if we can take the trade or not based on the rules
    '''

    def __init__(self, balance: float):
        self.balance = balance
        self.redis_client = RedisClient.get_instance()
        self.monitor = Monitoring.get_instance()
        self.lock = asyncio.Lock()
        self.counter = 0

    def get_trade_amount(self):
        return self.balance * (config.PERCENT_MAX_LOSS_PER_DAY / 100)

    async def validate_signal(self, signal: dict):
        # logger.info(f'Received {signal}')
        self.counter += 1
        logger.info(f'Call count: {self.counter} and trade status: {config.IN_TRADE}')
        balance = self.get_trade_amount()
        if not balance:
            logger.info('Zero Balance. Please funding your trading account')
            return
        
        trade_type, price, sl, instrument_token = signal['type'], signal['price'], signal['sl'], signal['instrument_token']

        risk_per_share = sl
        risk_per_trade = self.get_trade_amount()
        qty = int(risk_per_trade/risk_per_share)
        if not qty:
            logger.info('Stop Loss is too big')
            return
        
        order = {
            'transaction_type': trade_type,
            'quantity': qty,
            'price': price,
            'sl':sl,
            'instrument_token': instrument_token
        }
        # Store in redis that a trade is sent for execution so no more trades to execute
        # async with self.lock:
        #     is_set = await self.redis_client.setnx('in_trade', 'true')
        #     if is_set:
        #         await self.redis_client.publish('trade_signal', json.dumps(order))
        #         logger.info('Trade signal publish. Now will execute for all the users')
        #     else:
        #         logger.info('One Trade is running. So cannot execute another trade')

        # in_trade = await self.redis_client.get('in_trade')
        # if in_trade is None or in_trade == 'false':
        #     await self.redis_client.set(name='in_trade', value='true')
        #     # publish the trade on redis so that bot can execute it for all the users.
        #     await self.redis_client.publish('trade_signal', json.dumps(order))
        #     logger.info('Trade signal publish. Now will execute for all the users')
        #     # asyncio.run(self.broker.send_order(order))
        # else:
        #     logger.info('One Trade is running. So cannot execute another trade')

        if config.IN_TRADE == False:
            config.IN_TRADE = True
            # publish the trade on redis so that bot can execute it for all the users.
            await self.redis_client.publish('trade_signal', json.dumps(order))
            logger.info(f'Trade signal publish. Now will execute for all the users and Trade status {config.IN_TRADE}')
            # asyncio.run(self.broker.send_order(order))
        else:
            logger.info('One Trade is running. So cannot execute another trade')


