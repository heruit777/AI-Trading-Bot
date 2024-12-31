import asyncio
import ssl
import uuid
import pathlib
from websockets.asyncio.client import connect
from config import instrument_keys
import json

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
ssl_context.load_verify_locations(localhost_pem)

async def main():
    async with connect('wss://localhost:8765', ssl=ssl_context) as ws:
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
            print(json.loads(tick_data))

if __name__ == "__main__":
    asyncio.run(main())