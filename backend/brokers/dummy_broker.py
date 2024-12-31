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
from backend.config import instrument_keys, BALANCE

class Dummy_Broker(Broker):
    def __init__(self, access_token: str, api_version: str):
        self.access_token = access_token
        self.api_version = api_version
        self.redis_client = RedisClient.get_instance()
        self.monitor = Monitoring.get_instance()
        self.market_prices = {}

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
        """Fetch market data using WebSocket and print it."""
        # Establish connection to WebSocket
        async with await self.connect() as websocket:
            print('Connection established')

            await asyncio.sleep(1)  # Wait for 1 second

            # Data to be sent over the WebSocket
            data = {
                "guid": str(uuid.uuid4()),
                "method": "sub",
                "data": {
                    "mode": "ltpc",
                    "instrumentKeys": [instrument_keys['Reliance']]
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
                self.market_prices['Reliance'] = data_dict['feeds'][instrument_keys['Reliance']]['ltpc']['ltp']
                self.redis_client.publish('Reliance', json.dumps(data_dict))
                print('Published')
                # await asyncio.sleep(1)
                # Print the dictionary representation
                # print(json.dumps(data_dict))

    def get_balance(self):
        return BALANCE
    
    async def send_order(self, order):
        res1 = await self.send_market_order(order)
        if res1['status'] == 'success':
            if order['transaction_type'] == 'buy':
                order['price'] = res1['price'] - order['sl']
            else:
                # sell
                order['price'] = res1['price'] + order['sl']
            # print('From 103 line', order)
            order['trigger_price'] = order['price']
            del order['price']
            res2 = await self.send_stop_loss_market_order(order)
            if res2['status'] == 'success':
                self.monitor.monitor_trade(res1, res2)
    
    async def send_market_order(self, order:dict):
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
        market_price = self.market_prices['Reliance']
        # may be log it
        order_id = uuid.uuid4().int % (10**13)
        print(f'Market Order [{order_id}] placed successfully by Dummy Broker')
        return {'status': 'success', 'order_id': order_id, 'price': market_price}

    async def send_limit_order(self, order: dict):
        data = {
            'quantity': order['quantity'],
            'product': 'I',
            'validity': 'DAY',
            'price': order['price'],
            'instrument_token': order['instrument_token'],
            'order_type': 'LIMIT',
            'transaction_type': order['transaction_type'],
            'disclosed_quantity': 0,
            'trigger_price': 0, # It is for Stop loss orders only so it's irrelevant here
            'is_amo': False,
        }

        # Simulate http request
        await asyncio.sleep(0.5)
        # may be log it
        order_id = uuid.uuid4().int % (10**13)
        print(f'Limit Order [{order_id}] placed successfully by Dummy Broker')
        return {'status': 'success', 'order_id': order_id}

    async def send_stop_loss_market_order(self, order: dict):
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
        print(f'Stop Loss Market Order [{order_id}] placed successfully by Dummy Broker')
        return {'status': 'success', 'order_id': order_id, 'trigger_price': order['trigger_price']}
        

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
                # print(json.loads(tick_data))
                self.redis_client.publish('Reliance', tick_data)
                tick_data = json.loads(tick_data)
                self.market_prices['Reliance'] = tick_data['feeds'][instrument_keys['Reliance']]['ltpc']['ltp']
                print('Published')