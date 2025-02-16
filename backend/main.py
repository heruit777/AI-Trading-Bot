# import os
# from dotenv import load_dotenv
# from backend.brokers.dummy_broker import Dummy_Broker
# from backend.brokers.upstoxBroker import UpstoxBroker
# from backend.strategies.strategy1 import MovingAverageStrategy
# from backend.bot.Bot import Bot

# load_dotenv(override=True)
# access_token = os.getenv('UPSTOX_ACCESS_TOKEN')
# api_version = '2.0'
# broker = Dummy_Broker(access_token, api_version)
# strategy = MovingAverageStrategy(broker)
# bot = Bot(broker, strategy)
# bot.run()