# import talib as tb
# from talib import abstract
# import yfinance as yf
# import pandas as pd
# import numpy as np

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
# print(tb.MACD(np.array(c).flatten(), fastperiod=12, slowperiod=26, signalperiod=9))
# print(c)

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
# print(close_prices)
# # Calculate MACD
# macd, macd_signal, macd_hist = talib.MACD(close_prices, fastperiod=12, slowperiod=26, signalperiod=9)

# # Add MACD values to the DataFrame
# df['MACD'] = macd
# df['MACD_Signal'] = macd_signal
# df['MACD_Hist'] = macd_hist

# print(df)



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

# print(df)

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

import httpx
import csv
from config import instrument_keys


instrument_name = "Reliance"
interval = "day"
from_date = "2024-12-27"
to_date = "2022-12-27"
url = f'https://api.upstox.com/v2/historical-candle/{instrument_keys[instrument_name]}/{interval}/{from_date}/{to_date}'
headers = {
    'Accept': 'application/json',
}

response = httpx.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    candles = data["data"]["candles"]
    column_names = ["Timestamp", "Open", "High", "Low", "Close", "Volume", "Open Interest"]

    with open(f'{instrument_name}_{interval}_{from_date}_{to_date}.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(column_names)
        writer.writerows(candles)
    print('Data written successfully')
    
else:
    print(f"Error: {response.status_code} - {response.text}")