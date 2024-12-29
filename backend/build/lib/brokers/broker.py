# Abstract class for all the brokers
from typing import Callable
from abc import ABC, abstractmethod

class Broker(ABC):

    @abstractmethod
    def connect(self):
        """Method to establish a connection."""
        pass
    
    @abstractmethod
    def fetch_market_data(self, on_tick: Callable[[dict], None]):
        """Method to fetch market data from the broker."""
        pass
    