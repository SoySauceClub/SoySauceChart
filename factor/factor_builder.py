import os
import pandas as pd
import datetime

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

    @staticmethod
    def get_frog_info(df, ticker, hybrid_multiplier=0.7, target_folder=r'C:\temp\daily\factor'):
        file_path = os.path.join(target_folder, ticker + '.csv')
        fdf = pd.read_csv(file_path, parse_dates=True, index_col=0)
        dates_df = df.groupby(df.index.map(lambda x: x.date)).count()
        fdf = fdf[fdf.index.isin(dates_df.index)]
        df['Date'] = df.index.date
        fdf['Date'] = fdf.index.date
        df['DateTime'] = df.index
        temp_df = pd.merge(df, fdf[['Date', 'AvgRange', 'FrogBox']], how='left', on='Date').set_index(keys='DateTime')
        temp_df.loc[temp_df.index.time > datetime.time(10,0), ['AvgRange', 'FrogBox']] = None
        temp_df['RangeStat'] = temp_df['AvgRange'] + temp_df['FrogBox']
        temp_df['HybridFrog'] = temp_df['FrogBox'] * hybrid_multiplier
        return temp_df['RangeStat'], temp_df['HybridFrog'], temp_df['FrogBox']


