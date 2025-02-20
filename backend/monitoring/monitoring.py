from backend.redis_client import RedisClient
import backend.config as config
from backend.logger_config import logger
from backend.db.db import insert_trade_to_db, get_brokerId, update_balance
import json
from datetime import datetime
import asyncio
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
        # self.orders = [] # Trades that are live
        # self.cover_orders = [] # Trades that are still in pending status (not live yet)
        self.user_to_orders: dict[str, list[list]] = {}
        self.history: dict[str, list] = {}
        self.is_monitor = False

    def is_user_to_order_valid(self):
        if not self.user_to_orders: return False
        for value in self.user_to_orders.values():
            if value: # if this is not empty array, it's a valid value
                return True
        return False

    def get_order_details(self, userId: str):
        if userId not in self.user_to_orders: return None
        if not self.user_to_orders[userId]: return None
        transaction_type, mkt_order, sl_order, tp_order, pnl, now = self.user_to_orders[userId][0]
        return {'transaction_type': transaction_type, 'order_price': mkt_order['price'], 'sl_price': sl_order['trigger_price'], 'tp_price': tp_order['trigger_price'], 'pnl': pnl, 'qty': mkt_order['quantity'], 'ltp': self.currentStockPrice, 'time': now.strftime('%H:%M:%S')}
    
    async def subscribe_to_ticks(self):
        pubsub = self.redis_client.pubsub()
        await pubsub.subscribe('Reliance')

        async for message in pubsub.listen():
            if message['type'] == 'message':
                asyncio.create_task(self.process_tick_data(json.loads(message['data'])))

    def update_history(self, userId: str):
        # logger.info(f'Orders len = {len(self.user_to_orders[userId])}') => give 1 for each user
        transaction_type, mkt_order, sl_order, tp_order, pnl, now = self.user_to_orders[userId].pop(0) # each user will have atmost 1 trade only.
        # print('Line 44: monitoring.py', mkt_order, sl_order)
        if userId in self.history:
            self.history[userId].append({'transaction_type': transaction_type, 'order_price': mkt_order['price'], 'sl_price': sl_order['trigger_price'], 'tp_price': tp_order['trigger_price'], 'pnl': pnl, 'qty': mkt_order['quantity'], 'time': now.strftime('%H:%M:%S')})
        else:
            self.history[userId] = [{'transaction_type': transaction_type, 'order_price': mkt_order['price'], 'sl_price': sl_order['trigger_price'], 'tp_price': tp_order['trigger_price'], 'pnl': pnl, 'qty': mkt_order['quantity'], 'time': now.strftime('%H:%M:%S')}]
        print(f'updated history for {userId}')
        # remove order and cover order and place it in history 
        # order = self.orders.pop(0) # This can be an issue in future.
        # cover_order = self.cover_orders.pop(0)
        # if userId in self.history:
        #     self.history[userId].append({'order': order, 'cover_order': cover_order})
        # else:
        #     self.history[userId] = [{'order': order, 'cover_order': cover_order}]
    
    async def update_db(self, userId: str, qty: int, mk_price: float, ltp: float, pnl: float, transaction_type: str, time: datetime):
        # print(f'Trade entry done [{userId}]')
        brokerId = await get_brokerId(userId)
        print(f'Broker [{brokerId}]')
        await insert_trade_to_db(brokerId, 'Reliance', qty, mk_price, ltp, pnl, transaction_type, time)
        await update_balance(userId, pnl)

    async def close_trade(self, userId: str, qty: int, mk_price: float, ltp: float, 
                          pnl: float, transaction_type: str, time: datetime):
        self.update_history(userId)
        await self.update_db(userId, qty, mk_price, ltp, pnl, transaction_type, time)

    async def process_tick_data(self, tick_data: dict):
        ltp = tick_data['feeds'][config.instrument_keys['Reliance']]['ltpc']['ltp']
        self.currentStockPrice = ltp
        for userId, orders in self.user_to_orders.items():
            if not orders: continue

            # print(orders)
            transaction_type, mkt_order, sl_order, tp_order, pnl, now = orders[0]
            sl_price = sl_order['trigger_price']
            tp_price = tp_order['trigger_price']
            mk_price = mkt_order['price']
            qty = mkt_order['quantity']
            if transaction_type == 'buy':
                # update pnl
                self.user_to_orders[userId][0][4] = (ltp - mk_price) * qty
                if ltp <= sl_price:
                    print(f'SL triggered for Order Id: [{sl_order['order_id']}], User Id: [{userId}]')
                    await self.close_trade(userId, qty, mk_price, ltp, (ltp - mk_price) * qty, transaction_type, now)
                if ltp >= tp_price:
                    print(f'TP hit for Order Id: [{tp_order['order_id']}], User Id: [{userId}]')
                    await self.close_trade(userId, qty, mk_price, ltp, (ltp - mk_price) * qty, transaction_type, now)
            else:
                # update pnl
                self.user_to_orders[userId][0][4] = (mk_price - ltp) * qty
                if ltp >= sl_price:
                    print(f'SL triggered for Order Id: [{sl_order['order_id']}], User Id: [{userId}]')
                    await self.close_trade(userId, qty, mk_price, ltp, (mk_price - ltp) * qty, transaction_type, now)
                if ltp <= tp_price:
                    print(f'TP hit for Order Id: [{tp_order['order_id']}], User Id: [{userId}]')
                    await self.close_trade(userId, qty, mk_price, ltp, (mk_price - ltp) * qty, transaction_type, now)

        # logger.info(f'From Monitoring Module: Reliance ltp: {ltpc['ltp']} and ltq: {ltpc['ltq']}')
        # logic to monitor pl of orders
        # for trade in self.cover_orders:
        #     if trade['transaction_type'] == 'buy':
        #         # logger.info(f'{ltpc} {trade['order']['trigger_price']}')
        #         if ltpc <= trade['order']['trigger_price']:
        #             userId, orderId = trade['order']['user_id'], trade['order']['order_id']
        #             logger.info(f'SL trigger for Order Id: [{orderId}], User Id: [{userId}]')
        #             self.update_history(userId)
        #     else:
        #         if ltpc >= trade['order']['trigger_price']:
        #             userId, orderId = trade['order']['user_id'], trade['order']['order_id']
        #             logger.info(f'SL trigger for Order Id: [{orderId}], User Id: [{userId}]')
        #             self.update_history(userId)

        # if no trades are being monitored then you can update the redis in_trade variable to false
        # logger.info(f'orders: {self.orders} and cover_orders: {self.cover_orders}')
        if self.is_monitor and not self.is_user_to_order_valid():
            config.IN_TRADE = False
            self.is_monitor = False

    def monitor_trade(self, transaction_type: Literal['buy', 'sell'], userId: str, orders: list[dict]):
        '''
            orders: [mkt_order, sl_order, tp_order]
        '''
        # Will take two order
        print(f'monitoring is started')
        self.is_monitor = True
        mkt_order, sl_order, tp_order = orders
        if userId in self.user_to_orders:
            self.user_to_orders[userId].append([transaction_type, mkt_order, sl_order, tp_order, 0, datetime.now()])
        else:
            self.user_to_orders[userId] = [[transaction_type, mkt_order, sl_order, tp_order, 0, datetime.now()]]
        
        # print(self.get_order_details(userId))
        
        # self.orders.append({'transaction_type': transaction_type, 'order': order})
        # self.cover_orders.append({'transaction_type': transaction_type, 'order': sl_order})

        
    