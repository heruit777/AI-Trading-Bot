import asyncio
import ssl
import random
import pathlib
import json
import time
from websockets.asyncio.server import serve
from websocket import WebSocket
from backend.logger_config import logger
import backend.config as config


'''
RECEIVE:
{
    "guid": str(uuid.uuid4()),
    "method": "sub",
    "data": {
        "mode": "ltpc",
        "instrumentKeys": [instrument_keys['Reliance']]
    }
}
SEND:
{'feeds': {'NSE_EQ|INE002A01018': {'ltpc': {'ltp': 1210.7, 'ltt': '1735554551732', 'ltq': '16', 'cp': 1221.05}}}, 'currentTs': '1735568565831'}
'''

def get_amt():
    amt = round(random.random(), 2)
    mul = random.randint(0,1)
    mul = -1 if mul == 1 else 1
    price = (amt * mul)
    return round(price, 2)

async def send_tick_data(ws: WebSocket):
    data = await ws.recv()
    data = json.loads(data)
    instrument_name = data['data']['instrumentKeys']
    print(instrument_name)
    price = 1210.70
    while True:
        price += get_amt()
        price = round(price, 2)
        ltpc = {
            'ltp': price,
            'ltt': int(time.time() * 1000),
            'ltq': random.randint(1, 100),
            'cp':  price
        }
        await asyncio.sleep(0.1)
        tick_data = {
            'feeds': {
                config.instrument_keys[instrument_name]: {
                    'ltpc': {**ltpc}
                }
            }, 
            'currentTs': int(time.time() * 1000)
        }
        await ws.send(json.dumps(tick_data))
        print(f'>> {tick_data}')
    


ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
ssl_context.load_cert_chain(localhost_pem)

async def main():
    logger.info("Websocket Server Started on wss://localhost:8765")
    async with serve(send_tick_data, "localhost", 8765, ssl=ssl_context) as server:
        await server.serve_forever()  # run forever

if __name__ == "__main__":
    asyncio.run(main())