# Abstract class for all the brokers
from typing import Callable
from abc import ABC, abstractmethod

class Broker(ABC):

    @abstractmethod
    def send_order(self, userId: str, order: dict) -> dict:
        """Method to send a limit order and a Stop loss market order"""
        pass

    @abstractmethod
    def send_market_order(self, userId: str, order: dict) -> dict:
        """Method to send a market order"""
        pass

    def send_limit_order(self, userId: str, order: dict) -> dict:
        """Method to send a limit order"""
        pass

    def send_stop_loss_market_order(self, userId: str, order: dict) -> dict:
        """Method to send a stop loss market order"""
        pass
    
    @abstractmethod
    def fetch_and_publish_ticks(self):
        """Method to fetch market data from the broker."""
        pass

    @abstractmethod
    def demo_fetch_and_publish_ticks(self):
        """Method to fetch market data from my dummy_ws_server"""
        pass
    