class FactorBuilder(object):
    def __init__(self):
        pass

    @staticmethod
    def get_daily_open(df):
        open_prices = df.groupby(df.index.map(lambda x: x.date)).first()['Open'].tolist()
        price_counts = df.groupby(df.index.map(lambda x: x.date)).count()['Open'].tolist()
        price_list = []
        for open_price, price_count in zip(open_prices, price_counts):
            price_list.extend([open_price] * (price_count - 1))
            price_list.append(None)
        return price_list

    @staticmethod
    def get_bollinger_band(df, window=30, numsd=2):
        avg_ = df['Close'].rolling(window=window).mean()
        std_ = df['Close'].rolling(window=window).std()
        return avg_, avg_ + numsd*std_, avg_ - numsd*std_

