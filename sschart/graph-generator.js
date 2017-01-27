var GraphGenerator = (function () {
	function GraphGenerator(){}
    GraphGenerator.prototype.GenerateGraph = function(containerSelector, title, seriesData, graphSetUp, tradeData) {
        for (var i = 0; i < seriesData.length; i++) {
            if (seriesData[i].type == 'ohlc') {
                seriesData[i].events = {
                    click : function(event) {
                        point = event.point;
                        console.log();
                        tradeData.push({
                            time: point.x,
                            open: point.open,
                            close: point.close,
                            high: point.high,
                            low: point.low,
                            title, title
                        })
                        this.chart.xAxis[0].addPlotLine({
                            color: 'red',
                            dashStyle: 'solid',
                            width: 1,
                            value: point.x
                        });
                    }
                };
                break;
            }
        }
        $(containerSelector).highcharts('StockChart', {

            rangeSelector: {
                enabled: true
            },

            title: {
                text: title
            },
			legend: {
           		enabled: true,
           		layout: 'horizontal',
           		maxHeight: 100,
          	},
            yAxis: [{
                labels: {
                    align: 'right',
                    x: -3
                },
                title: {
                    text: graphSetUp.yAxis[0].title
                },
                scrollbar: {
                    enabled: true
                },
                lineWidth: 2,
                tickInterval: 0.02,
				scalable: true,
				offset: 50
            }],
			tooltip: {
				valueDecimals: 2,
				enabled: true,
				followTouchMove: false,
				positioner: function () {
                    return { x: 0, y: 0 };
                }
            },
            series: seriesData,
        });
    };
    return GraphGenerator;
}());