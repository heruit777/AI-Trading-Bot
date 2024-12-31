from abc import ABC, abstractmethod

class TradingStrategy(ABC):
    
    @abstractmethod
    def subscribe_to_ticks(self):
        pass

    @abstractmethod
    def process_tick_data(self, tick_data: dict):
        pass
