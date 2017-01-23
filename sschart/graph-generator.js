var GraphGenerator = (function () {
	function GraphGenerator(){}
    GraphGenerator.prototype.GenerateGraph = function(containerSelector, title, seriesData, graphSetUp) {
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
            series: seriesData
        });
    };
    return GraphGenerator;
}());