import upstox_client
import asyncio
import json
import os
import pathlib
import ssl
import httpx
import uuid
import websockets
import backend.brokers.MarketDataFeed_pb2 as pb
from google.protobuf.json_format import MessageToDict
from backend.brokers.broker import Broker
import backend.config as config
from backend.logger_config import logger
from backend.redis_client import RedisClient

class UpstoxBroker(Broker):
    def __init__(self, access_token: str, api_version: str):
        self.access_token = access_token
        self.api_version = api_version
        self.base_url = 'https://api-hft.upstox.com/v2'
        self.redis_client = RedisClient.get_instance()
        self.set_configuration()
        
    def set_configuration(self):
        self.configuration = upstox_client.Configuration()
        self.configuration.access_token = self.access_token
        self.api_client = upstox_client.ApiClient(self.configuration)
        self.user = upstox_client.UserApi(self.api_client)
        
    def connect(self):
        """Connect to the Upstox WebSocket."""
        # Create default SSL context
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        response = self.get_market_data_feed_authorize()

        # Connect to the WebSocket with SSL context
        return websockets.connect(response.data.authorized_redirect_uri, ssl=ssl_context)
    
    def get_market_data_feed_authorize(self):
        """Get authorization for market data feed."""
        api_instance = upstox_client.WebsocketApi(
            self.api_client
        )
        api_response = api_instance.get_market_data_feed_authorize(self.api_version)
        return api_response
    
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
                await self.redis_client.publish('Reliance', json.dumps(data_dict))
                logger.info('Published')
                # await asyncio.sleep(1)
                # logger.info the dictionary representation
                # logger.info(json.dumps(data_dict))

    def get_balance(self):
        thread = self.user.get_user_fund_margin(self.api_version, async_req=True)
        logger.info(thread.get())


    async def send_order(self, userId: str, order: dict):
        logger.info('Sending order to upstox require real money.')

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

        url = f'{self.base_url}/order/place'

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            if response.status_code == 200:
                data = response.json()
                order_id = data['data']['order_id']
                logger.info(f'Market Order [{order_id}] placed successfully by Upstox Broker')
                #send the order_id to monitoring module

    async def send_limit_order(self, userId: str, order: dict):
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

        url = f'{self.base_url}/order/place'

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            if response.status_code == 200:
                data = response.json()
                order_id = data['data']['order_id']
                logger.info(f'Limit Order [{order_id}] placed successfully by Upstox Broker')

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

        url = f'{self.base_url}/order/place'

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            if response.status_code == 200:
                data = response.json()
                order_id = data['data']['order_id']
                logger.info(f'Stop Loss Market Order [{order_id}] placed successfully by Upstox Broker')

            

    # For my dummy_ws_server(Mock websocket server that send tick data)
    def demo_connect(self):
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        localhost_pem = pathlib.Path(os.path.dirname(__file__)).with_name("localhost.pem")
        ssl_context.load_verify_locations(localhost_pem)
    
        return websockets.connect('wss://localhost:8765', ssl=ssl_context)
    
    # For my dummy_ws_server(Mock websocket server that send tick data)
    async def demo_fetch_and_publish_ticks(self):
        async with self.demo_connect() as ws:
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
                await self.redis_client.publish('Reliance', tick_data)
                logger.info('Published')
    
