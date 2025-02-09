# import talib as tb
# from talib import abstract
# import yfinance as yf
# import pandas as pd
# import numpy as np
# from backend.logger_config import logger

# data = yf.download('RELIANCE.NS', start='2024-12-01', end='2024-12-08', interval='15m')
# day_data = data.first("3D")

# day_data = {
#     "close": day_data["Adj Close"].values.flatten(),
#     "high": day_data["High"].values.flatten(),
#     "low": day_data["Low"].values.flatten(),
#     "open": day_data["Open"].values.flatten(),
#     "volume": day_data["Volume"].values.flatten()
# }
# fun = abstract.Function('MACD')
# c = fun(day_data, signalperiod=1)
# logger.info(tb.MACD(np.array(c).flatten(), fastperiod=12, slowperiod=26, signalperiod=9))
# logger.info(c)

# import talib
# import numpy as np
# import pandas as pd

# # Example stock price data
# data = {
#     "close": [10, 10.5, 10.7, 10.9, 11, 11.3, 11.6, 11.8, 12, 12.2]
# }
# df = pd.DataFrame(data)

# # Convert closing prices to a NumPy array
# close_prices = np.array(df['close'])
# logger.info(close_prices)
# # Calculate MACD
# macd, macd_signal, macd_hist = talib.MACD(close_prices, fastperiod=12, slowperiod=26, signalperiod=9)

# # Add MACD values to the DataFrame
# df['MACD'] = macd
# df['MACD_Signal'] = macd_signal
# df['MACD_Hist'] = macd_hist

# logger.info(df)



# import talib
# from talib import abstract
# import numpy as np
# import pandas as pd

# # Example stock data as a DataFrame
# data = {
#     "open": [100.0, 102, 104, 103, 105],
#     "high": [105, 106.2, 108, 107, 109],
#     "low": [95, 98, 102.4, 100, 103],
#     "close": [102, 105, 103.4, 106, 108],
#     "volume": [1000, 1100, 1200, 1300, 1400],
# }
# df = pd.DataFrame(data)

# # Convert to dictionary-like structure for Abstract API
# input_data = {
#     "open": df["open"].values,
#     "high": df["high"].values,
#     "low": df["low"].values,
#     "close": df["close"].values,
#     "volume": df["volume"].values,
# }

# # Example 1: Using MACD (Moving Average Convergence Divergence)
# macd_func = abstract.Function("MACD")
# macd, macd_signal, macd_hist = macd_func(input_data)

# # Example 2: Using RSI (Relative Strength Index)
# rsi_func = abstract.Function("RSI")
# rsi = rsi_func(input_data, timeperiod=14)

# # Add the results back to the DataFrame
# df["MACD"] = macd
# df["RSI"] = rsi

# logger.info(df)

# import logging

# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S"
# )


# logging.debug("This is a debug message")
# logging.info("This is a info message", extra={"user_id": 23, "order_id": 55})
# logging.warning("This is a warning message")
# logging.debug("This is debug message")
# logging.error("This is a error message")
# logging.critical("This is a critical message")

# To fetch historical candle data of a particular instrument at a specific interval and save it in csv file

# import httpx
# import csv
# from config import instrument_keys


# instrument_name = "Reliance"
# interval = "day"
# from_date = "2024-12-27"
# to_date = "2022-12-27"
# url = f'https://api.upstox.com/v2/historical-candle/{instrument_keys[instrument_name]}/{interval}/{from_date}/{to_date}'
# headers = {
#     'Accept': 'application/json',
# }

# response = httpx.get(url, headers=headers)
# if response.status_code == 200:
#     data = response.json()
#     candles = data["data"]["candles"]
#     column_names = ["Timestamp", "Open", "High", "Low", "Close", "Volume", "Open Interest"]

#     with open(f'{instrument_name}_{interval}_{from_date}_{to_date}.csv', mode='w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(column_names)
#         writer.writerows(candles)
#     logger.info('Data written successfully')
    
# else:
#     logger.info(f"Error: {response.status_code} - {response.text}")

# connect to Redis
# import redis

# redis_server = redis.Redis(host="localhost", port="6379")
# redis_server.set(name='foo', value='bar')

# logger.info('Value set, retrieve it')

# value = redis_server.get('foo')
# logger.info(f'Value for foo is {value}')

# from decimal import Decimal

# balance = 0.1 * (2/100)
# # balance = Decimal(str(balance))
# # distance = Decimal('0.1')
# distance = 0.1
# ans = round(balance+distance, 4)
# ans += 0.000150

# logger.info(ans)


# Fetch Portfolio stream feed

# import upstox_client
# import ssl
# import websockets
# import asyncio
# import json
# import os
# from dotenv import load_dotenv

# load_dotenv()


# def get_portfolio_stream_feed_authorize(api_version, configuration):
#     api_instance = upstox_client.WebsocketApi(
#         upstox_client.ApiClient(configuration))
#     api_response = api_instance.get_portfolio_stream_feed_authorize(
#         api_version)
#     return api_response


# async def fetch_order_updates():
#     ssl_context = ssl.create_default_context()
#     ssl_context.check_hostname = False
#     ssl_context.verify_mode = ssl.CERT_NONE

#     # Configure OAuth2 access token for authorization: OAUTH2
#     configuration = upstox_client.Configuration()

#     api_version = '2.0'
#     configuration.access_token = os.getenv('UPSTOX_ACCESS_TOKEN')

#     # Get portfolio stream feed authorize
#     response = get_portfolio_stream_feed_authorize(
#         api_version, configuration)

#     async with websockets.connect(response.data.authorized_redirect_uri, ssl=ssl_context) as websocket:
#         logger.info('Connection established')

#         # Perform WebSocket operations
#         while True:
#             message = await websocket.recv()
#             logger.info(json.dumps(message))

# asyncio.run(fetch_order_updates())


# class Monitoring():
#     '''
#         To check if the trade hit SL or TP
#     '''
#     _instance = None

#     @classmethod
#     def get_instance(cls):
#         if not cls._instance:
#             cls._instance = Monitoring()
#         return cls._instance
    
#     def __new__(cls, *args, **kwargs):
#         if cls._instance is not None:
#             raise Exception("This is a singleton class. Use `get_instance()` to access the instance.")
#         return super().__new__(cls)

#     # don't use the constructor to create the objects
#     def __init__(self):
#         self.running_trades = [] # Trades that are live
#         self.pending_trades = [] # Trades that are still in pending status (not live yet)

# a = Monitoring.get_instance()
# b = Monitoring.get_instance()
# a.running_trades.append(10)
# logger.info(a.running_trades)
# logger.info(b.running_trades)