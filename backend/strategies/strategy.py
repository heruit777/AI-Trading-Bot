from abc import ABC, abstractmethod

class TradingStrategy(ABC):
    
    @abstractmethod
    def process_tick_data(self, tick_data: dict):
        pass