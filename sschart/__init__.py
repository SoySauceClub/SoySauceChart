import simplejson as json
import pandas as pd
import pandas_datareader.data as web
import numpy as np
from factor.factor_builder import FactorBuilder
from sschart.graph_series import GraphSeries
from sschart.graph_html_generator import GraphHtmlGenerator

if __name__ == '__main__':
    start_date = '20150101'
    end_date = '20150201'
    ticker = 'AAPL'

    target_price = r'c:\temp\1minute\price\{0}.csv'.format(ticker)
    price_df = pd.read_csv(target_price, parse_dates=True, index_col=0)
    price_df = price_df.loc[price_df.index >= pd.to_datetime(start_date)]
    price_df = price_df.loc[price_df.index <= pd.to_datetime(end_date)]
    original_df = price_df.copy()
    price_df['DailyOpen'] = FactorBuilder.get_daily_open(original_df)
    price_df['MA30'], price_df['BB30_1U'], price_df['BB30_1B'] = FactorBuilder.get_bollinger_band(original_df, 30, 1)
    _, price_df['BB30_2U'], price_df['BB30_2B'] = FactorBuilder.get_bollinger_band(original_df, 30, 2)
    _, price_df['BB30_3U'], price_df['BB30_3B'] = FactorBuilder.get_bollinger_band(original_df, 30, 3)
    price_df['RangeStat'], price_df['HybridFrog'], price_df['FrogBox'] = FactorBuilder.get_frog_info(
        original_df,
        ticker,
        hybrid_multiplier=0.7
    )
    price_df['RangeStatUp'] = price_df['DailyOpen'] + price_df['RangeStat']
    price_df['RangeStatDown'] = price_df['DailyOpen'] - price_df['RangeStat']
    price_df['HybridFrogUp'] = price_df['DailyOpen'] + price_df['HybridFrog']
    price_df['HybridFrogDown'] = price_df['DailyOpen'] - price_df['HybridFrog']

    #define the series that you want here, the pandas data frame need to contain the headers
    series1 = GraphSeries(name='OHLC', headers=['DateTime', 'Open', 'High', 'Low', 'Close'], seriestype='ohlc')
    series2 = GraphSeries(name='MA30', headers=['DateTime', 'MA30'], seriestype='line')
    series3 = GraphSeries(name='DailyOpen-line', headers=['DateTime', 'DailyOpen'], seriestype='line')
    series4 = GraphSeries(name='BB1', headers=['DateTime', 'BB30_1U', 'BB30_1B'], seriestype='arearange')
    series5 = GraphSeries(name='BB2', headers=['DateTime', 'BB30_2U', 'BB30_2B'], seriestype='arearange')
    series6 = GraphSeries(name='BB3', headers=['DateTime', 'BB30_3U', 'BB30_3B'], seriestype='arearange')
    series7 = GraphSeries(name='RangeStatUp', headers=['DateTime', 'DailyOpen', 'RangeStatUp'], seriestype='arearange')
    series8 = GraphSeries(name='RangeStatDown', headers=['DateTime', 'DailyOpen', 'RangeStatDown'], seriestype='arearange')
    series9 = GraphSeries(name='HybridBoxUp', headers=['DateTime', 'DailyOpen', 'HybridFrogUp'], seriestype='arearange')
    series10 = GraphSeries(name='HybridBoxDown', headers=['DateTime', 'DailyOpen', 'HybridFrogDown'], seriestype='arearange')
    graphSetUp = [
        series1,
        series2,
        series3,
        series4,
        series5,
        series6,
        series7,
        series8,
        series9,
        series10
    ]

    graphSetUpJson = json.dumps([ob.__dict__ for ob in graphSetUp])
    dataInJson = price_df.reset_index().to_json(orient='records')

    with open('set_up.json', 'w') as f:
        f.write(graphSetUpJson)

    with open('data.json', 'w') as f:
        f.write(dataInJson)

    print(dataInJson)

    template_folder = r'C:\github\SoySauceChart\sschart'
    # template_folder = r'I:\Projects\SoySauceChart\sschart'
    template_name = 'Chart-template.html'
	#change this to whatever folder that you want to store the result html
    export_path = r'C:\temp\chart_result\test123.html'

    generator = GraphHtmlGenerator(template_folder=template_folder, template_name=template_name)
    generator.generate_html_with_json(price_json_data=dataInJson, graph_setup_data=graphSetUpJson, export_path=export_path)
    print('Done!')
