from backend.brokers.broker import Broker
from backend.config import PERCENT_MAX_LOSS_PER_DAY
from backend.redis_client import RedisClient
from backend.monitoring.monitoring import Monitoring
import asyncio

class Risk_Management():
    '''
        It take signal and check if we can take the trade or not based on the rules
    '''

    def __init__(self, broker: Broker):
        self.broker = broker
        self.redis = RedisClient.get_instance()
        self.monitor = Monitoring.get_instance()

    @staticmethod
    def get_trade_amount(balance: float):
        return balance * (PERCENT_MAX_LOSS_PER_DAY / 100)

    def validate_signal(self, signal: dict):
        # print(f'Received {signal}')
        balance = self.broker.get_balance()
        if not balance:
            print('Zero Balance. Please funding your trading account')
            return
        
        trade_type, price, sl, instrument_token = signal['type'], signal['price'], signal['sl'], signal['instrument_token']

        risk_per_share = sl
        risk_per_trade = self.get_trade_amount(balance)
        qty = int(risk_per_trade/risk_per_share)
        if not qty:
            print('Stop Loss is too big')
            return
        
        order = {
            'transaction_type': trade_type,
            'quantity': qty,
            'price': price,
            'sl':sl,
            'instrument_token': instrument_token
        }
        # Store in redis that a trade is sent for execution so no more trades to execute
        in_trade = self.redis.get('in_trade')
        if in_trade is None or in_trade == 'false':
            self.redis.set(name='in_trade', value='true')
            asyncio.run(self.broker.send_order(order))
        else:
            print('One Trade is running. So cannot execute another trade')


