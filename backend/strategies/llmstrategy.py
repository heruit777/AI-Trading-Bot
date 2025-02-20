from backend.redis_client import RedisClient
import backend.config as config
from datetime import date, time, datetime, timedelta
from jsonschema import validate
from backend.logger_config import logger
from dateutil.relativedelta import relativedelta
import pandas as pd
import ta
import json
import httpx
from groq import AsyncGroq
import os
import asyncio
from dotenv import load_dotenv

load_dotenv(override=True)

class LLMStrategy():
    def __init__(self):
        self.redis_client = RedisClient.get_instance()
        self.window = 7 # used in RSI and EMA, how much candles to consider
        self.timeframe = '30minute'
        # Strategy will run between these timings
        self.start_time = time(9, 40, 0) # keeping a buffer time of 7 minutes
        self.stop_time = time(15, 10, 0)

    async def subscribe_to_ticks(self):
        pubsub = self.redis_client.pubsub()
        await pubsub.subscribe('Reliance')

        print('LLM strategy has subscribed')
        await asyncio.gather(
            self.listen_to_ticks(pubsub),
            self.run()
        )

    async def listen_to_ticks(self, pubsub):
        async for message in pubsub.listen():
            if message['type'] == 'message':
                tick_data = json.loads(message['data'])
                ltp = tick_data['feeds'][config.instrument_keys['Reliance']]['ltpc']['ltp']
                self.mkt_price = ltp


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
    The user will provide stock data which will have open, high, low, close, volumne, RSI (window {self.window}) and EMA (window {self.window}). The time frame will be {self.timeframe}. Focus more on price action, support and resistance, trend rather than on technical indicators(consider them for additional confirmation). The stock data will be from oldest to newest(recent candle data will be at the last). Based on this data, analyze the stock and tell me whether the stock will go up(buy) or down (sell), provide a trade recommendation in JSON format. Following is the JSON schema:
    {{
        "trade_type": 'buy' or 'sell' (required) (Should I go `buy` or `sell` based on the market will go up or down?),
        "confidence_score": int (0-100) (required) (How confident are you in this trade?)
    }}
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
    
    async def get_historical_data(self):
        # get the candle data for past 15 days
        today = date.today()
        old_date = today - relativedelta(days=15)
        today = today.isoformat()
        url = f"https://api.upstox.com/v2/historical-candle/{config.instrument_keys['Reliance']}/30minute/{today}/{old_date}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        data = response.json()

        if data["status"] != "success":
            print('The request was not successful.')
            return None
        return data['data']['candles']
    
    async def get_intraday_candles(self):
        # fetch today's candles and update the candle array above
        interval = "30minute"
        url = f"https://api.upstox.com/v2/historical-candle/intraday/{config.instrument_keys['Reliance']}/{interval}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        data = response.json()

        if data["status"] != "success":
            print('The request was not successful.')
            return None
        return data['data']['candles']
    
    async def publish_trade(self, trade: dict):
        sl, tp = 4, 8
        signal = {'type': trade['trade_type'], 'price': self.mkt_price, 'sl': sl, 'tp': tp, 'instrument_token': config.instrument_keys['Reliance']}
        # sl = abs(trade['entry_price']-trade['stop_loss'])
        # tp = abs(trade['entry_price']-trade['target_price'])
        # signal = {'type': trade['trade_type'], 'price': trade['entry_price'], 'sl': sl, 'tp': tp, 'instrument_token': config.instrument_keys['Reliance']}
        logger.info(f'Trade found: {signal} and Trade status: {config.IN_TRADE}')
        # publish the trade signal on redis so that bot can do risk analysis for all the users.
        await self.redis_client.publish('trade_signal', json.dumps(signal))
        logger.info(f'Trade signal publish. Now will do risk analysis for each user')

    def check_time(self):
        now_time = datetime.now().time()
        
        if now_time < self.start_time or now_time > self.stop_time:
            print(f'Strategy only runs between {self.start_time} to {self.stop_time}')
            return False
        return True
    
    async def core_logic(self):
        try:
            historical_candles = await self.get_historical_data() # array of candles
            print(f'Historical candles: {historical_candles}')
            if not historical_candles: 
                raise Exception('Error occured in fetching historical candles')
            
            intraday_candles = await self.get_intraday_candles()
            print(f'intraday candles: {intraday_candles}')
            if not intraday_candles: 
                raise Exception('Error occured in fetching intraday candles')

            data = intraday_candles + historical_candles
            print(f'candles data: {data}')
            data = self.transform(data)
            print(f'data: {data}')
            sys_prompt = self.get_sys_prompt()
            trade, reason = await self.get_llm_answer(sys_prompt, data)
            trade = json.loads(trade)
            schema = {
                "type" : "object",
                "properties" : {
                    "trade_type" : {"type" : "string"},
                    "confidence_score" : {"type" : "number"}
                },
            }
            validate(instance=trade, schema=schema)
            print(trade, reason)
            if trade['confidence_score'] >= 0: # >= 75
                print(f'Good trade {trade}')
                await self.publish_trade(trade)
            else:
                print(f'No trade taken because {trade['confidence_score']} < 75')
        except Exception as e:
            print(f'Some error occured {e}')

    async def run(self):
        try:
            timings: list[datetime] = []
            start = datetime.combine(datetime.today(), self.start_time)
            start += timedelta(minutes=7)
            stop = datetime.combine(datetime.today(), self.stop_time)

            while start <= stop:
                timings.append(start)
                start = start + timedelta(minutes=30)

            # For test purpose, if you don't want to wait for the next 30 minute you can append the current time 
            # it will execute trade on that time.
            # timings.append(datetime.today().replace(hour=12, minute=1, second=0, microsecond=0))
            isDone = [False] * len(timings)
            print(timings, isDone)
            while True:
                if not self.check_time():
                    asyncio.sleep(0.1)
                    continue

                now = datetime.now().replace(second=0, microsecond=0)
                await asyncio.sleep(0.1)
                for index, value in enumerate(timings):
                    # print(now, index, value)
                    if now == value and isDone[index] == False:
                        print('RUNNING core logic')
                        isDone[index] = True
                        await self.core_logic()
                    
                    
        except Exception as e:
            print(f'Some error occured {e}')
            
if __name__ == "__main__":
    a = LLMStrategy()
    # asyncio.run(a.test_run())
    asyncio.run(a.run())
        