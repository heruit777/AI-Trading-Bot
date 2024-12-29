from broker import Broker
import upstox_client
import asyncio
import json
import ssl
import uuid
import websockets
from google.protobuf.json_format import MessageToDict
import MarketDataFeed_pb2 as pb
from config import instrument_keys
from typing import Callable

class UpstoxBroker(Broker):
    def __init__(self, access_token: str, api_version: str):
        self.access_token = access_token
        self.api_version = api_version
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
    
    async def fetch_market_data(self, on_tick: Callable[[dict], None]):
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
                    "mode": "full",
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
                on_tick(data_dict)
                # Print the dictionary representation
                # print(json.dumps(data_dict))
    
