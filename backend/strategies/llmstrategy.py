'''
    In this strategy, I will use Groq 'deepseek-r1-distill-llama-70b' model's api. The prompt will contain
    - 100 candles of 30min OHLC, Volume, RSI, EMA
    Output:
    {
        "trade_type": 'long' or 'short' (required) (Should I go `long` or `short`?),
        "entry_price": float (required) (The best price to enter the trade),
        "stop_loss": float (required) (A price level to exit if the trade goes wrong),
        "target_price": float (required) (A realistic profit-taking price),
        "confidence_score": int (0-100) (required) (How confident are you in this trade?)
    }
    ONLY Trade if confidence is >= 75%
'''

from backend.redis_client import RedisClient
import backend.config as config
from datetime import date
from backend.logger_config import logger
from dateutil.relativedelta import relativedelta
from backend.risk_management.risk_management import Risk_Management
import pandas as pd
import ta
import httpx
from groq import AsyncGroq
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

class LLMStrategy():
    def __init__(self):
        self.redis_client = RedisClient.get_instance()
        self.risk_manager = Risk_Management(balance=config.BALANCE)
        self.window = 7 # used in RSI and EMA, how much candles to consider
        self.timeframe = '30minute'

    def transform(self, candles: list):
        open_prices = [candle[1] for candle in candles]
        high_prices = [candle[2] for candle in candles]
        low_prices = [candle[3] for candle in candles]
        close_prices = [candle[4] for candle in candles]
        volumes = [candle[5] for candle in candles]
        data = pd.DataFrame({
            'open': open_prices,
            'high': high_prices,
            'low': low_prices,
            'close': close_prices,
            'volume': volumes
        })
        # Reverse the DataFrame so the oldest candle appears first
        data = data.iloc[::-1].reset_index(drop=True)
        data['RSI'] = ta.momentum.rsi(data['close'], window=self.window)
        data['EMA'] = ta.trend.ema_indicator(data['close'], window=self.window)
        data = data.iloc[self.window:].reset_index(drop=True)
        arr = []
        for _, row in data.iterrows():
            arr.append(row.to_dict())
        return arr
   
    def get_sys_prompt(self):
        return  f'''
    The user will provide stock data which will have open, high, low, close, volumne, RSI (window {self.window}) and EMA (window {self.window}). The time frame will be {self.timeframe}. Focus more on price action, support and resistance, trend rather than on technical indicators(consider them for additional confirmation). The stock data will be from oldest to newest(recent candle data will be at the last). Based on this data, analyze the stock and provide a trade recommendation in JSON format. Following is the JSON schema:
    {{
        "trade_type": 'long' or 'short' (required) (Should I go `long` or `short`?),
        "entry_price": float (required) (The best price to enter the trade),
        "stop_loss": float (required) (A price level to exit if the trade goes wrong),
        "target_price": float (required) (A realistic profit-taking price),
        "confidence_score": int (0-100) (required) (How confident are you in this trade?)
    }}
    Remember trade recommendation are for Intraday basis so keep Stop loss and target_price based on the volatility of the stock.
    '''

    async def get_llm_answer(self, sys_prompt: str, data: list):
        client = AsyncGroq(api_key=os.getenv('GROQ_API_KEY'))
        response = await client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        response_format={"type": "json_object"},
        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": f'Following is the stock data {data}'}
        ]
        )
        message = response.choices[0].message
        return [message.content, message.reasoning]


    async def core_logic(self):
        # get the candle data to pass to LLM
        today = date.today()
        old_date = today - relativedelta(days=15)
        today = today.isoformat()
        url = f"https://api.upstox.com/v2/historical-candle/{config.instrument_keys['Reliance']}/30minute/{today}/{old_date}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        data = response.json()

        if data["status"] != "success":
            print('The request was not successful.')
            return 

        candles = data['data']['candles'] # array of candles
        data = self.transform(candles)
        print(data)
        sys_prompt = self.get_sys_prompt()
        trade, reason = await self.get_llm_answer(sys_prompt, data)
        print(trade, reason)
        if trade['confidence_score'] >= 75:
            # send trade for risk management validation
            pass
    '''
    DEMO RESPONSE
    {
  "trade_type": "short",
  "entry_price": 1266.0,
  "stop_loss": 1271.0,
  "target_price": 1250.0,
  "confidence_score": 70
} Alright, so I need to analyze the provided stock data and make a trade recommendation. The user has given me a list of stock data with open, high, low, close, volume, RSI (7-period), and EMA (7-period). The time frame is 30 minutes, and the focus should be more on price action, support, and resistance rather than the technical indicators, although they can be used for confirmation.

First, I'll start by looking at the overall trend. I notice that the stock has been moving in an uptrend for most of the data, but there are some pullbacks and consolidations. The latest candles show some bearish signs, so I need to see if that's a reversal or just a temporary dip.

Looking at the price action, the recent candles have lower highs and lower lows, which could indicate a potential downtrend or a correction. The volume has been increasing during these dips, which might suggest selling pressure. However, the RSI is around 38, which is in the oversold region, so there might be a bounce coming.

I should identify support and resistance levels. The recent low around 1263 seems to be a support level, but it was broken in the last few candles. The next support could be around 1250, which is a significant level from earlier data. On the resistance side, 1280 has been a resistance point, and the price is struggling to go above that.

The EMA is also a consideration. The EMA is at 1268, which is slightly below the current price, indicating that the trend is still bearish but not too strong. The RSI being oversold might mean a short-term bounce, but the overall trend is bearish.

Considering all this, it might be a good time to go short, targeting the next support level. The entry price would be around the current price where the bearish momentum is strong. The stop loss should be just above the recent high to avoid getting caught in a sudden upswing. The target price would be the next support level, which is around 1250. The confidence is moderate because while the indicators suggest a bearish move, the oversold RSI could lead to a pullback.

I should also consider the volatility. Since it's a 30-minute time frame, the stop loss and target shouldn't be too tight. A 20-30 point stop loss and a 50-60 point target seem reasonable based on recent price movements.

So, putting it all together, the recommendation would be to go short with an entry around 1266, stop loss at 1271, target at 1250, and a confidence score of 70.
    '''
            
if __name__ == "__main__":
    a = LLMStrategy()
    asyncio.run(a.core_logic())
        