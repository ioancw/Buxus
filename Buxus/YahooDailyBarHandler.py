import pandas as pd
import numpy as np
from pandas_datareader import data as web


class YahooDailyBarHandler(object):
    def __init__(self, ticker, start_date, end_date, event_queue):
        self.symbol = ticker
        self.start = start_date
        self.end = end_date
        self.event_queue = event_queue
        self.continue_backtest = True
        self.get_data()
        self.bar_stream = self.get_ticker_data()

    def get_data(self):
        ''' Retrieves and prepares the data.
        '''
        raw = web.DataReader(self.symbol, data_source='yahoo', start=self.start, end=self.end)['Adj Close']
        raw = pd.DataFrame(raw)
        raw.rename(columns={'Adj Close': 'price'}, inplace=True)
        raw['return'] = np.log(raw / raw.shift(1))
        self.data = raw.dropna()

    def get_ticker_data(self):
        return self.data.itertuples()

    def stream_next(self):
        """
        Place the next BarEvent onto the event queue.
        """
        try:
            row = next(self.bar_stream)
        except StopIteration:
            self.continue_backtest = False
            return

        self.event_queue.put(row)