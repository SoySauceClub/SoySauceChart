import os
import pandas as pd
import simplejson as json
import datetime
from factor.factor_builder import FactorBuilder
from sschart.graph_html_generator import GraphHtmlGenerator
from sschart.chart_style import ChartStyle

class SingleChart(object):
    def __init__(self, data_json, graph_setup_json, global_setup_json):
        self.data = data_json
        self.graphSetUp = graph_setup_json
        self.globalSetUp = global_setup_json

    def to_json(self):
        return '{' + 'seriesData:{0}, graphSetUp:{1}, globalSetUp: {2}'\
            .format(self.data, self.graphSetUp, self.globalSetUp) + '}'

class GraphSeries(object):
    def __init__(self, name, headers, seriestype, y_axis=0, style_setup=None):
        self.name = name
        self.headers = headers
        self.seriestype = seriestype
        self.yAxis = y_axis
        self.style_setup = style_setup


class GraphSetup(object):
    def __init__(self, start_date, end_date, ticker, data_folder_root, trade_file, indicator_list, list_all):
        self.start_date = start_date
        self.end_date = end_date
        self.ticker = ticker
        self.one_minute_price_folder = os.path.join(data_folder_root, '1minute', 'price')
        self.one_minute_factor_folder = os.path.join(data_folder_root, '1minute', 'factor')
        self.daily_price_folder = os.path.join(data_folder_root, 'daily', 'price')
        self.daily_factor_folder = os.path.join(data_folder_root, 'daily', 'factor')
        self.trade_file = trade_file
        self.frog_multiplier = self._get_frog_multiplier(indicator_list)
        self.graphics = self._setup_graphics(indicator_list)
        self.price_df = self._build_chart_data()

        #added by Liang Guo
        self.list_all = list_all
        self.price_dfs = []
        self.tickers = []
        if list_all:
            self.tickers = map(lambda file_name: file_name.split('.')[0], os.listdir(self.one_minute_price_folder))
            self.price_dfs = map(self._build_chart_data, self.tickers)

    def save_chart(self, output_folder, title_addition, subchart):
        if subchart or self.list_all:
            if self.list_all:
                multi_charts_json = self.build_multi_charts_json(title_addition, self.price_dfs)
            else:
                multi_charts_json = self.build_multi_charts_json(title_addition)
            self._save(multi_charts_json, self.start_date, self.end_date, output_folder)
        else:
            charts = self.build_charts(title_addition)
            self._save(charts, self.start_date, self.end_date, output_folder)

    def build_multi_charts_json(self, title_addition, price_dfs=None):
        multi_charts = []
        price_dfs = [self.price_df] if price_dfs is None else self.price_dfs
        for index, price_df in enumerate(price_dfs):
            start_date = self.start_date
            self.ticker = self.tickers[index]
            while int(start_date) <= int(self.end_date):
                end_date = GraphSetup._next_weekday(pd.to_datetime(start_date), 6).strftime('%Y%m%d')
                current_price_df = price_df[(price_df.index >= pd.to_datetime(start_date))
                                         & (price_df.index <= pd.to_datetime(end_date))]
                single_chart_data = self._construct_single_chart(current_price_df, start_date, end_date, title_addition)
                multi_charts.append(single_chart_data)
                start_date = end_date
        multi_charts_json = '[' + ','.join([x.to_json() for x in multi_charts]) + ']'
        return multi_charts_json

    def build_charts(self, title_addition):
        single_chart_data = self._construct_single_chart(self.price_df, self.start_date, self.end_date, title_addition)
        charts = '[' + single_chart_data.to_json() + ']'
        return charts

    def _construct_single_chart(self, price_df, start_date, end_date, title_addition):
        graph_global_setup = {
                'title': self.ticker + ' ' + title_addition + ' from  ' + start_date + ' to ' + end_date,
                'yAxis': [{'title': 'Price'}]
            }
        graph_set_up_json = json.dumps([ob.__dict__ for ob in self.graphics])
        data_in_json = price_df.reset_index().to_json(orient='records')
        global_set_up_json = json.dumps(graph_global_setup)
        single_chart_data = SingleChart(data_in_json, graph_set_up_json, global_set_up_json)
        return single_chart_data

    def _save(self, price_df, start_date, end_date, title_addition, output_folder):
        template_folder = r'.\sschart'
        template_name = r'Chart-template.html'
        graph_global_setup = {
            'title': self.ticker + ' ' + title_addition + ' from  ' + start_date + ' to ' + end_date,
            'yAxis': [{'title': 'Price'}]
        }
        graph_set_up_json = json.dumps([ob.__dict__ for ob in self.graphics])
        data_in_json = price_df.reset_index().to_json(orient='records')
        global_set_up_json = json.dumps(graph_global_setup)
        export_path = os.path.join(output_folder, '{0}_{1}_{2}.html'.format(self.ticker, start_date, end_date))
        generator = GraphHtmlGenerator(template_folder=template_folder, template_name=template_name)
        generator.generate_html_with_json(price_json_data=data_in_json, graph_setup_data=graph_set_up_json,
                                          graph_global_setup=global_set_up_json, export_path=export_path)

    def _save(self, multiple_charts, start_date, end_date, output_folder):
        template_folder = r'.\sschart'
        template_name = r'Chart-template.html'
        data = multiple_charts
        title = 'all' if self.list_all else self.ticker
        export_path = os.path.join(output_folder, '{0}_{1}_{2}.html'.format(title, start_date, end_date))
        generator = GraphHtmlGenerator(template_folder=template_folder, template_name=template_name)
        generator.generate_html_with_json(charts_json_data=data, export_path=export_path)

    def _get_frog_multiplier(self, indicator_list):
        frog_multiplier = 0
        for indicator in indicator_list:
            if indicator.startswith('Frog'):
                frog_multiplier = float(indicator.replace('Frog', ''))
        return frog_multiplier

    def _setup_graphics(self, indicator_list):
        ohlc = GraphSeries(name='OHLC', headers=['DateTime', 'Open', 'High', 'Low', 'Close'], seriestype='ohlc',
                           style_setup=ChartStyle.OHLC_STYLE)
        ma30 = GraphSeries(name='MA30', headers=['DateTime', 'MA30'], seriestype='line')
        daily_open = GraphSeries(name='DailyOpen', headers=['DateTime', 'DailyOpen'], seriestype='line')
        bb_1_std = GraphSeries(name='BB1', headers=['DateTime', 'BB30_1U', 'BB30_1B'], seriestype='arearange',
                               style_setup=ChartStyle.AREA_STYLE)
        bb_2_std = GraphSeries(name='BB2', headers=['DateTime', 'BB30_2U', 'BB30_2B'], seriestype='arearange',
                               style_setup=ChartStyle.AREA_STYLE)
        bb_3_std = GraphSeries(name='BB3', headers=['DateTime', 'BB30_3U', 'BB30_3B'], seriestype='arearange',
                               style_setup=ChartStyle.AREA_STYLE)
        rs_up = GraphSeries(name='RangeStatUp', headers=['DateTime', 'DailyOpen', 'RangeStatUp'],
                            seriestype='arearange',
                            style_setup=ChartStyle.RANGE_STAT_AREA_STYLE)
        rs_down = GraphSeries(name='RangeStatDown', headers=['DateTime', 'DailyOpen', 'RangeStatDown'],
                              seriestype='arearange', style_setup=ChartStyle.RANGE_STAT_AREA_STYLE)
        hf_up = GraphSeries(name='HybridBoxUp', headers=['DateTime', 'DailyOpen', 'HybridFrogUp'],
                            seriestype='arearange',
                            style_setup=ChartStyle.FROG_AREA_STYLE)
        hf_down = GraphSeries(name='HybridBoxDown', headers=['DateTime', 'DailyOpen', 'HybridFrogDown'],
                              seriestype='arearange',
                              style_setup=ChartStyle.FROG_AREA_STYLE)
        rl_10 = GraphSeries(name='RegLine10', headers=['DateTime', 'RegLine10'], seriestype='line')
        rl_30 = GraphSeries(name='RegLine30', headers=['DateTime', 'RegLine30'], seriestype='line')
        rl_90 = GraphSeries(name='RegLine90', headers=['DateTime', 'RegLine90'], seriestype='line')
        rl_270 = GraphSeries(name='RegLine270', headers=['DateTime', 'RegLine270'], seriestype='line')
        long_trade = GraphSeries(name='Long', headers=['DateTime', 'LongPrice'], seriestype='scatter')
        short_trade = GraphSeries(name='Short', headers=['DateTime', 'ShortPrice'], seriestype='scatter')
        graph_setup = [ohlc, daily_open]

        if 'RangeStat' in indicator_list:
            graph_setup.extend([rs_up, rs_down])

        if any([t.startswith('Frog') for t in indicator_list]):
            graph_setup.extend([hf_up, hf_down])

        if 'BB' in indicator_list:
            graph_setup.extend([ma30, bb_1_std, bb_2_std, bb_3_std])

        if 'RegLine' in indicator_list:
            graph_setup.extend([rl_10, rl_30, rl_90, rl_270])

        if self.trade_file is not None:
            graph_setup.extend([long_trade, short_trade])

        return graph_setup

    def _build_chart_data(self, ticker=None):
        if ticker is None:
            ticker = self.ticker
        target_price_path = os.path.join(self.one_minute_price_folder, ticker + '.csv')
        price_df = pd.read_csv(target_price_path, parse_dates=True, index_col=0)
        price_df = price_df.loc[price_df.index >= pd.to_datetime(self.start_date)]
        price_df = price_df.loc[price_df.index <= pd.to_datetime(self.end_date)]
        original_df = price_df.copy()
        price_df['DailyOpen'] = FactorBuilder.get_daily_open(original_df)
        price_df['MA30'], price_df['BB30_1U'], price_df['BB30_1B'] = FactorBuilder.get_bollinger_band(
            original_df, 30, 1)
        _, price_df['BB30_2U'], price_df['BB30_2B'] = FactorBuilder.get_bollinger_band(original_df, 30, 2)
        _, price_df['BB30_3U'], price_df['BB30_3B'] = FactorBuilder.get_bollinger_band(original_df, 30, 3)
        price_df['RangeStat'], price_df['HybridFrog'], price_df['FrogBox'] = FactorBuilder.get_frog_info(
            original_df,
            ticker,
            hybrid_multiplier=self.frog_multiplier,
            target_folder=self.daily_factor_folder
        )
        price_df['RangeStatUp'] = price_df['DailyOpen'] + price_df['RangeStat']
        price_df['RangeStatDown'] = price_df['DailyOpen'] - price_df['RangeStat']
        price_df['HybridFrogUp'] = price_df['DailyOpen'] + price_df['HybridFrog']
        price_df['HybridFrogDown'] = price_df['DailyOpen'] - price_df['HybridFrog']
        price_df['RegLine10'], price_df['RegLine30'], price_df['RegLine90'], price_df['RegLine270'] = FactorBuilder \
            .get_regression_line_info(original_df, ticker, target_folder=self.one_minute_factor_folder)

        if self.trade_file is not None:
            price_df['LongPrice'], price_df['ShortPrice'] = FactorBuilder.get_trade_info(original_df, self.trade_file)

        return price_df

    @staticmethod
    def _next_weekday(d, weekday):
        """
        Get the next date
        :param d: the TimeStamp object of the date to be processed
        :param weekday: int, 0 next Monday, 1 next Tuesday ... 6 next Sunday
        :return: TimeStamp of next date
        """
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return d + datetime.timedelta(days_ahead)