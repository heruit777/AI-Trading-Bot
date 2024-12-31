import os
import asyncio
from dotenv import load_dotenv
from brokers.broker import Broker
from brokers.upstoxBroker import UpstoxBroker
from brokers.dummy_broker import Dummy_Broker
from strategies.strategy1 import MovingAverageStrategy
from strategies.strategy import TradingStrategy
from backend.monitoring.monitoring import Monitoring
from concurrent.futures import ThreadPoolExecutor


class Bot():
    '''
        Main interaction point. This will utilize all the other classes
    '''
    def __init__(self, broker: Broker, strategy: TradingStrategy):
        self.broker = broker
        self.strategy = strategy
        self.monitor = Monitoring.get_instance()

    async def helper(self):
        loop = asyncio.get_running_loop()
        executor = ThreadPoolExecutor(5)
        
        await asyncio.gather(
            loop.run_in_executor(executor, self.strategy.subscribe_to_ticks),
            loop.run_in_executor(executor, self.monitor.subscribe_to_ticks),
            # self.broker.demo_fetch_and_publish_ticks()
            self.broker.fetch_and_publish_ticks()
        )

    def run(self):
        asyncio.run(self.helper())    


# Dependency Injection for strategy
load_dotenv()
access_token = os.getenv('UPSTOX_ACCESS_TOKEN')
api_version = '2.0'
broker = Dummy_Broker(access_token, api_version)
strategy = MovingAverageStrategy(broker)
bot = Bot(broker, strategy)
bot.run()
