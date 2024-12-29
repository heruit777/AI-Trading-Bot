from strategy import TradingStrategy

class MovingAverageStrategy(TradingStrategy):
    def process_tick_data(self, tick_data: dict):
        print('From trading strategy 1')
        print(tick_data)