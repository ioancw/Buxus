import queue as queue
from YahooDailyBarHandler import YahooDailyBarHandler


class TradingSession(object):
    def __init__(self, event_queue, start_date, end_date, ticker):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.event_queue = event_queue
        self.price_handler = YahooDailyBarHandler(self.ticker,
                                                  self.start_date,
                                                  self.end_date,
                                                  self.event_queue)

    def start_trading(self):
        self._run_session()

    def _run_session(self):
        while self.price_handler.continue_backtest:
            try:
                event = event_queue.get(False)
            except queue.Empty:
                self.price_handler.stream_next()
            else:
                if event is not None:
                    print(event)
                    # If backtesting then call calculate signals method on strategy object


if __name__ == "__main__":
    event_queue = queue.Queue()
    trading_session = TradingSession(event_queue, '2010-01-01', '2011-01-01', 'DIS')
    trading_session.start_trading()