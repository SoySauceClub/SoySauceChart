import os
import pandas as pd
import numpy as np
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
        try:
            fdf = pd.read_csv(file_path, parse_dates=True, index_col=0)
        except IOError:
            return None, None, None
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

    @staticmethod
    def get_regression_line_info(df, ticker, target_folder=r'C:\temp\1minute\factor'):
        file_path = os.path.join(target_folder, ticker + '.csv')
        try:
            fdf = pd.read_csv(file_path, parse_dates=True, index_col=0)
        except IOError:
            return None, None, None, None
        sliced_fdf = fdf[fdf.index.isin(df.index)]
        return sliced_fdf['RegLine10'], sliced_fdf['RegLine30'], sliced_fdf['RegLine90'], sliced_fdf['RegLine270']

    @staticmethod
    def get_trade_info(df, trade_path):
        tdf = pd.read_csv(trade_path, parse_dates=False)
        tdf['EntryDateTime'] = pd.to_datetime(tdf['EntryDate'] + ' ' + tdf['EntryTime'])
        tdf['ExitDateTime'] = pd.to_datetime(tdf['ExitDate'] + ' ' + tdf['ExitTime'])
        tdf['LongDateTime'] = np.where(tdf['Direction'] == 'LONG', tdf['EntryDateTime'], tdf['ExitDateTime'])
        tdf['LongPrice'] = np.where(tdf['Direction'] == 'LONG', tdf['EntryPrice'], tdf['ExitPrice'])
        tdf['ShortDateTime'] = np.where(tdf['Direction'] == 'SHORT', tdf['EntryDateTime'], tdf['ExitDateTime'])
        tdf['ShortPrice'] = np.where(tdf['Direction'] == 'SHORT', tdf['EntryPrice'], tdf['ExitPrice'])
        df['LongPrice'] = np.nan
        df['ShortPrice'] = np.nan
        buy_tdf = tdf[tdf['LongDateTime'].isin(df.index)]
        sell_tdf = tdf[tdf['ShortDateTime'].isin(df.index)]
        df.loc[df.index.isin(buy_tdf['LongDateTime']), 'LongPrice'] = buy_tdf['LongPrice'].tolist()
        df.loc[df.index.isin(sell_tdf['ShortDateTime']), 'ShortPrice'] = buy_tdf['ShortPrice'].tolist()
        return df['LongPrice'], df['ShortPrice']
