# take the data from websockets
# Import necessary modules
import asyncio
import json
import ssl
import upstox_client
import websockets
import uuid
import os
from backend.logger_config import logger
from dotenv import load_dotenv
import backend.config as config
from google.protobuf.json_format import MessageToDict

import backend.brokers.MarketDataFeed_pb2 as pb

load_dotenv()
access_token = os.getenv('UPSTOX_ACCESS_TOKEN')

def get_market_data_feed_authorize(api_version, configuration):
    """Get authorization for market data feed."""
    api_instance = upstox_client.WebsocketApi(
        upstox_client.ApiClient(configuration))
    
    api_response = api_instance.get_market_data_feed_authorize(api_version)
    return api_response


def decode_protobuf(buffer):
    """Decode protobuf message."""
    feed_response = pb.FeedResponse()
    feed_response.ParseFromString(buffer)
    return feed_response


async def fetch_market_data():
    """Fetch market data using WebSocket and logger.info it."""

    # Create default SSL context
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Configure OAuth2 access token for authorization
    configuration = upstox_client.Configuration()

    api_version = '2.0'
    configuration.access_token = access_token

    # Get market data feed authorization
    response = get_market_data_feed_authorize(
        api_version, configuration)

    # Connect to the WebSocket with SSL context
    async with websockets.connect(response.data.authorized_redirect_uri, ssl=ssl_context) as websocket:
        logger.info('Connection established')

        await asyncio.sleep(1)  # Wait for 1 second

        # Data to be sent over the WebSocket
        data = {
            "guid": str(uuid.uuid4()),
            "method": "sub",
            "data": {
                "mode": "full",
                "instrumentKeys": [config.instrument_keys['Reliance'], config.instrument_keys['TCS'], config.instrument_keys['HDFC BANK'], config.instrument_keys['ICICI BANK'], config.instrument_keys['BHARTI AIRTEL']]
            }
        }

        # Convert data to binary and send over WebSocket
        binary_data = json.dumps(data).encode('utf-8')
        await websocket.send(binary_data)

        # Continuously receive and decode data from WebSocket
        while True:
            message = await websocket.recv()
            decoded_data = decode_protobuf(message)

            # Convert the decoded data to a dictionary
            data_dict = MessageToDict(decoded_data)

            # logger.info the dictionary representation
            logger.info(json.dumps(data_dict))


# Execute the function to fetch market data
asyncio.run(fetch_market_data())