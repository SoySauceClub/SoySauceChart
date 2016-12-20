import click
from sschart.graph_series import GraphSeries, GraphSetup
from sschart.graph_html_generator import GraphHtmlGenerator
from sschart.chart_style import ChartStyle


@click.command()
@click.option('--ticker', default='AAPL', help='Ticker Symbol')
@click.option('--data_folder', default=r'.\sample_data', help='The minute bar folder root')
@click.option('--trade_file', default=None, help='The trade file that shows the actual trades')
@click.option('--out_folder', default=r'.', help='The folder that contains the output')
@click.option('--subchart/--non-subchart', default=True, help='Enable weekly range plot if needed')
@click.option('--start_date', default='20161109', help='Start date of the plotting')
@click.option('--end_date', default='20161110', help='End date of the plotting')
@click.option('--title_addition', default='Frog 0.7', help='Additional Chart Title Text')
@click.option('--indicators', default='RangeStat,Frog0.7',
              help='Indicator separated with comma: RangeStat,Frog[multiplier],BB,RegLine')
@click.option('--list-all', default=True, help='Display all tickers in data folder')
@click.option('--multiproc', help='For Pycharm debug only, no use')
@click.option('--qt-support', help='For Pycharm debug only, no use')
@click.option('--client', help='For Pycharm debug only, no use')
@click.option('--file', help='For Pycharm debug only, no use')
@click.option('--port', help='For Pycharm debug only, no use')
def main(ticker, data_folder, trade_file, out_folder, subchart, start_date, end_date, title_addition, indicators, list_all,
         multiproc, qt_support, client, file, port):
    indicator_list = indicators.split(',')
    graph_setup = GraphSetup(
        start_date=start_date,
        end_date=end_date,
        ticker=ticker,
        data_folder_root=data_folder,
        trade_file=trade_file,
        indicator_list=indicator_list,
        list_all=list_all
    )
    graph_setup.save_chart(output_folder=out_folder, title_addition=title_addition, subchart=subchart)

if __name__ == '__main__':
    main()