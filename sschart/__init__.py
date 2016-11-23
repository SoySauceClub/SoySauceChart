import simplejson as json
import pandas as pd
import pandas_datareader.data as web
import numpy as np
from factor.factor_builder import FactorBuilder
from sschart.graph_series import GraphSeries
from sschart.graph_html_generator import GraphHtmlGenerator

if __name__ == '__main__':
    start_date = '20161110'

    target_price = r'c:\temp\1minute\price\AAPL.csv'
    price_df = pd.read_csv(target_price, parse_dates=True, index_col=0)
    price_df = price_df.loc[price_df.index >= pd.to_datetime(start_date)]
    price_df['DailyOpen'] = FactorBuilder.get_daily_open(price_df)
    price_df['MA30'], price_df['BB30_2U'], price_df['BB30_2B'] = FactorBuilder.get_bollinger_band(price_df, 30, 2)
    _, price_df['BB30_1U'], price_df['BB30_1B'] = FactorBuilder.get_bollinger_band(price_df, 30, 1)

    #define the series that you want here, the pandas data frame need to contain the headers
    series1 = GraphSeries(name='OHLC', headers=['DateTime', 'Open', 'High', 'Low', 'Close'], seriestype='ohlc')
    series2 = GraphSeries(name='MA30', headers=['DateTime', 'MA30'], seriestype='line')
    series3 = GraphSeries(name='DailyOpen-line', headers=['DateTime', 'DailyOpen'], seriestype='line')
    series4 = GraphSeries(name='BB2', headers=['DateTime', 'BB30_2U', 'BB30_2B'], seriestype='arearange')
    series5 = GraphSeries(name='BB1', headers=['DateTime', 'BB30_1U', 'BB30_1B'], seriestype='arearange')
    graphSetUp = [series1, series2, series3, series4, series5]

    graphSetUpJson = json.dumps([ob.__dict__ for ob in graphSetUp])
    dataInJson = price_df.reset_index().to_json(orient='records')
    print(dataInJson)

    # template_folder = r'C:\github\SoySauceChart\sschart'
    template_folder = r'I:\Projects\SoySauceChart\sschart'
    template_name = 'Chart-template.html'
	#change this to whatever folder that you want to store the result html
    export_path = r'C:\temp\chart_result\test123.html'

    generator = GraphHtmlGenerator(template_folder=template_folder,
                                                         template_name=template_name)
    generator.generate_html_with_json(price_json_data=dataInJson, graph_setup_data=graphSetUpJson, export_path=export_path)
    print('Done!')
