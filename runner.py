import click
import logging
import sys
from datetime import datetime
from sschart.graph_series import GraphSetup

today = datetime.now().today()
today_str = today.strftime('%Y%m%d')

@click.command()
@click.option('--ticker', default=None, help='Ticker Symbol')
@click.option('--data_folder', default=r'.', help='The minute bar folder root')
@click.option('--trade_file', default=None, help='The trade file that shows the actual trades')
@click.option('--out_folder', default=r'.', help='The folder that contains the output')
@click.option('--subchart/--non-subchart', default=True, help='Enable weekly range plot if needed')
@click.option('--start_date', default=today_str, help='Start date of the plotting')
@click.option('--end_date', default=today_str, help='End date of the plotting')
@click.option('--title_addition', default='', help='Additional Chart Title Text')
@click.option('--indicators', default='RangeStat,Frog0.7',
              help='Indicator separated with comma: RangeStat,Frog[multiplier],BB,RegLine')
@click.option('--list-daily/--list-ticker', default=True, help='Display all tickers in data folder')
@click.option('--template_name', default=r'Chart-template.html', help='Specify the template name')
@click.option('--universe_path', default=None, help='An universe file to specify what tickers to plot')
@click.option('--debug/--no-debug', default=False, help='A flag to show debug info')
@click.option('--multiproc', help='For Pycharm debug only, no use')
@click.option('--qt-support', help='For Pycharm debug only, no use')
@click.option('--client', help='For Pycharm debug only, no use')
@click.option('--file', help='For Pycharm debug only, no use')
@click.option('--port', help='For Pycharm debug only, no use')
def main(ticker, data_folder, trade_file, out_folder, subchart, start_date, end_date, title_addition, indicators,
         list_daily, template_name, universe_path, debug, multiproc, qt_support, client, file, port):
    log = logging.getLogger()
    log_console = logging.StreamHandler(sys.stdout)
    log.setLevel(logging.DEBUG if debug else logging.INFO)
    log_console.setLevel(logging.DEBUG if debug else logging.INFO)
    log.addHandler(log_console)

    log.debug(str.format('ticker: {0}', ticker))
    log.debug(str.format('data_folder: {0}', data_folder))
    log.debug(str.format('trade_file: {0}', trade_file))
    log.debug(str.format('out_folder: {0}', out_folder))
    log.debug(str.format('subchart: {0}', subchart))
    log.debug(str.format('start_date: {0}', start_date))
    log.debug(str.format('end_date: {0}', end_date))
    log.debug(str.format('title_addition: {0}', title_addition))
    log.debug(str.format('indicators: {0}', indicators))
    log.debug(str.format('list-daily: {0}', list_daily))
    log.debug(str.format('template_name: {0}', template_name))
    log.debug(str.format('universe_path: {0}', universe_path))

    if ticker is not None and not list_daily:
        tickers = [ticker]
        log.debug('Processing single ticker time series')
    elif universe_path is not None and not list_daily:
        tickers = GraphSetup.get_instruments_from_file(universe_path)
        log.debug(str.format('Processing universe and list daily is {0}', list_daily))
    elif list_daily:
        tickers = ['DAILY']
        log.debug('Listing all tickers for the date')
    else:
        raise NotImplementedError('Need to specify at least a ticker / universe or use list_daily')

    for (i, t) in enumerate(tickers):
        log.info(str.format("Processing {0} ({1} out of {2}) ", t, i + 1, len(tickers)))
        indicator_list = indicators.split(',')
        graph_setup = GraphSetup(
            start_date=start_date,
            end_date=end_date,
            ticker=t,
            data_folder_root=data_folder,
            trade_file=trade_file,
            indicator_list=indicator_list,
            list_daily=list_daily,
            template_name=template_name,
            universe=universe_path
        )
        graph_setup.save_chart(output_folder=out_folder, title_addition=title_addition, subchart=subchart)

if __name__ == '__main__':
    main()
