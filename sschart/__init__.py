import json
import pandas as pd
import pandas_datareader.data as web
import numpy as np
from sschart.graph_series import GraphSeries
from sschart.graph_html_generator import GraphHtmlGenerator

if __name__ == '__main__':

    #you can construct whatever you want into pandas dataframe
    price_df = web.get_data_yahoo('EWZ', '10/28/2015', '10/31/2016')
    sLength = len(price_df['Open'])
    price_df['LR'] = pd.Series(np.random.randn(sLength), index=price_df.index)

    #define the series that you want here, the pandas data frame need to contain the headers
    series1 = GraphSeries(name='OHLC', headers=['Date', 'Open', 'High', 'Low', 'Close'], seriestype='candlestick')
    series2 = GraphSeries(name='Volumn', headers=['Date', 'Volume'], seriestype='column', yAxis=1)
    series3 = GraphSeries(name='LR-line', headers=['Date', 'LR'], seriestype='line')
    series4 = GraphSeries(name='AreaRange', headers=['Date', 'High', 'Low'], seriestype='arearange')
    graphSetUp = [series1, series2, series3, series4]

    graphSetUpJson = json.dumps([ob.__dict__ for ob in graphSetUp])
    dataInJson = price_df.reset_index().to_json(orient='records')
    print(dataInJson)
	#change this template_folder variable to the current folder
    template_folder = r'E:\GitHub\SoySauceChart\sschart'
    template_name = 'Chart-template.html'
	#change this to whatever folder that you want to store the result html
    export_path = r'C:\temp\chart_result\test123.html'

    generator = GraphHtmlGenerator(template_folder=template_folder,
                                                         template_name=template_name)
    generator.generate_html_with_json(price_json_data=dataInJson, graph_setup_data=graphSetUpJson, export_path=export_path)
    print('Done!')
