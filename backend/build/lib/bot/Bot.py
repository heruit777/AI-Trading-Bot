import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from Signal_Detection import Signal_Detection
from backend.brokers.broker import Broker
from brokers.upstoxBroker import UpstoxBroker
from strategies.strategy1 import MovingAverageStrategy

class Bot():
    '''
        Main interaction point. This will utilize all the other classes
    '''
    def __init__(self, broker: Broker):
        self.broker = broker
        self.signal_detector = Signal_Detection(self.broker, MovingAverageStrategy())

    def run(self):
        self.signal_detector.find()


# Dependency Injection for strategy
load_dotenv()
access_token = os.getenv('UPSTOX_ACCESS_TOKEN')
api_version = '2.0'
broker = UpstoxBroker(access_token, api_version)
bot = Bot(broker)
bot.run()


class Risk_Management():
    '''
        It take signal and check if we can take the trade or not based on the rules
    '''
    pass

class Execution():
    '''
        Send the order to the broker
    '''
    pass

class Monitoring():
    '''
        To check if the trade hit SL or TP
    '''
    pass


        
