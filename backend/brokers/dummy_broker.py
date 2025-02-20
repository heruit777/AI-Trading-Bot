'''
    The Dummy Broker will use upstox to fetch real time tick data so the code is same here.
'''

import os
import pathlib
import asyncio
import upstox_client
import ssl
import websockets
import uuid
import json
import backend.brokers.MarketDataFeed_pb2 as pb
from backend.redis_client import RedisClient
from google.protobuf.json_format import MessageToDict
from backend.brokers.broker import Broker
from backend.monitoring.monitoring import Monitoring
import backend.config as config
from backend.logger_config import logger

class Dummy_Broker(Broker):
    def __init__(self, access_token: str, api_version: str):
        self.access_token = access_token
        self.api_version = api_version
        self.redis_client = RedisClient.get_instance()
        self.monitor = Monitoring.get_instance()

    def get_market_data_feed_authorize(self):
        """Get authorization for market data feed."""
        configuration = upstox_client.Configuration()
        configuration.access_token = self.access_token
        api_instance = upstox_client.WebsocketApi(
            upstox_client.ApiClient(configuration)
        )
        api_response = api_instance.get_market_data_feed_authorize(self.api_version)
        return api_response


    def connect(self):
        """Connect to the Upstox WebSocket."""
        # Create default SSL context
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        response = self.get_market_data_feed_authorize()

        # Connect to the WebSocket with SSL context
        return websockets.connect(response.data.authorized_redirect_uri, ssl=ssl_context)
    
    def decode_protobuf(self, buffer):
        """Decode protobuf message."""
        feed_response = pb.FeedResponse()
        feed_response.ParseFromString(buffer)
        return feed_response
    
    async def fetch_and_publish_ticks(self):
        """Fetch market data using WebSocket and logger.info it."""
        # Establish connection to WebSocket
        async with await self.connect() as websocket:
            logger.info('Connection established')

            await asyncio.sleep(1)  # Wait for 1 second

            # Data to be sent over the WebSocket
            data = {
                "guid": str(uuid.uuid4()),
                "method": "sub",
                "data": {
                    "mode": "ltpc",
                    "instrumentKeys": [config.instrument_keys['Reliance']]
                }
            }

            # Convert data to binary and send over WebSocket
            binary_data = json.dumps(data).encode('utf-8')
            await websocket.send(binary_data)

            # Continuously receive and decode data from WebSocket
            while True:
                message = await websocket.recv()
                decoded_data = self.decode_protobuf(message)

                # Convert the decoded data to a dictionary
                data_dict = MessageToDict(decoded_data)
                price = data_dict['feeds'][config.instrument_keys['Reliance']]['ltpc']['ltp']
                # update the price in the hash map
                await self.redis_client.hset(config.INSTRUMENT_PRICES_KEY, "Reliance", price)
                await self.redis_client.publish('Reliance', json.dumps(data_dict))
                # logger.info('Published')
                # await asyncio.sleep(1)
                # logger.info the dictionary representation
                # logger.info(json.dumps(data_dict))
    
    async def send_order(self, userId, order):
        mkt_order = await self.send_market_order(userId, order)
        sl_price, tp_price = order['sl'], order['tp']
        if mkt_order['status'] == 'success':
            if order['transaction_type'] == 'buy':
                sl_price = mkt_order['price'] - sl_price
                tp_price = mkt_order['price'] + tp_price
            else:
                # sell
                sl_price = mkt_order['price'] + sl_price
                tp_price = mkt_order['price'] - tp_price

            order1, order2 = order.copy(), order.copy()
            
            order1['trigger_price'] = sl_price
            order2['trigger_price'] = tp_price
            # print('From 103 line', order, order1, sl_price, tp_price)
            # sl_order = await self.send_stop_loss_market_order(userId, order)
            # tp_order = await self.send_limit_order(userId, order1)
            sl_order, tp_order = await asyncio.gather(self.send_stop_loss_market_order(userId, order1), self.send_limit_order(userId, order2))
            if sl_order['status'] == 'success' and tp_order['status'] == 'success':
                self.monitor.monitor_trade(order['transaction_type'], userId, [mkt_order, sl_order, tp_order])
    
    async def send_market_order(self, userId: str, order:dict):
        data = {
            'quantity': order['quantity'],
            'product': 'I', # Intraday
            'validity': 'DAY',
            'price': 0,
            'instrument_token': order['instrument_token'],
            'order_type': 'MARKET',
            'transaction_type': order['transaction_type'],
            'disclosed_quantity': 0,
            'trigger_price': 0,
            'is_amo': False,
        }

        # Simulate http request
        await asyncio.sleep(0.5)
        # may be log it
        market_price = await self.redis_client.hget(config.INSTRUMENT_PRICES_KEY, "Reliance")
        order_id = uuid.uuid4().int % (10**13)
        logger.info(f'Market Order [{order_id}] placed successfully by Dummy Broker at {float(market_price)} for user id [{userId}]')
        return {'status': 'success', 'order_id': order_id, 'user_id': userId, 'price': float(market_price), 'quantity': order['quantity']}

    async def send_limit_order(self, userId: str, order: dict):
        data = {
            'quantity': order['quantity'],
            'product': 'I',
            'validity': 'DAY',
            'price': 0,
            'instrument_token': order['instrument_token'],
            'order_type': 'LIMIT',
            'transaction_type': order['transaction_type'],
            'disclosed_quantity': 0,
            'trigger_price': order['trigger_price'], 
            'is_amo': False,
        }

        # Simulate http request
        await asyncio.sleep(0.5)
        # may be log it
        order_id = uuid.uuid4().int % (10**13)
        logger.info(f'Limit Order [{order_id}] placed successfully by Dummy Broker')
        return {'status': 'success', 'user_id': userId, 'order_id': order_id, 'trigger_price': order['trigger_price']}

    async def send_stop_loss_market_order(self, userId: str, order: dict):
        data = {
            'quantity': order['quantity'],
            'product': 'I',
            'validity': 'DAY',
            'price': 0.0,
            'instrument_token': order['instrument_token'],
            'order_type': 'SL-M',
            'transaction_type': order['transaction_type'],
            'disclosed_quantity': 0,
            'trigger_price': order['trigger_price'],
            'is_amo': False,
        }

        # Simulate http request
        await asyncio.sleep(0.5)
        # may be log it
        order_id = uuid.uuid4().int % (10**13)
        logger.info(f'Stop Loss Market Order [{order_id}] placed successfully by Dummy Broker')
        return {'status': 'success', 'order_id': order_id, 'user_id': userId, 'trigger_price': order['trigger_price']}
        

    # For my dummy_ws_server(Mock websocket server that send tick data)
    def demo_connect(self):
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        localhost_pem = pathlib.Path(os.path.dirname(__file__)).with_name("localhost.pem")
        ssl_context.load_verify_locations(localhost_pem)
    
        return websockets.connect('wss://localhost:8765', ssl=ssl_context)
    
    # For my dummy_ws_server(Mock websocket server that send tick data)
    async def demo_fetch_and_publish_ticks(self):
        async with self.demo_connect()  as ws:
            data = {
                "guid": str(uuid.uuid4()),
                "method": "sub",
                "data": {
                    "mode": "ltpc",
                    "instrumentKeys": 'Reliance'
                }
            }
            await ws.send(json.dumps(data))
            while True:
                tick_data = await ws.recv()
                # logger.info(json.loads(tick_data))
                tick_data = json.loads(tick_data)
                price = tick_data['feeds'][config.instrument_keys['Reliance']]['ltpc']['ltp']
                # update the price in the hash map
                await self.redis_client.hset(config.INSTRUMENT_PRICES_KEY, "Reliance", price)
                # logger.info('Published')
                await self.redis_client.publish('Reliance', json.dumps(tick_data))