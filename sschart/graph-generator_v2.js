var GraphGenerator = (function () {
	function GraphGenerator(){}
	
	//decide location of time by binary search
	function locationOf(element, array, start, end) {
		start = start || 0;
		end = end || array.length;
		var pivot = parseInt(start + (end - start) / 2, 10);
		if (end-start <= 1 || array[pivot] === element) return pivot;
		if (array[pivot] < element) {
			return locationOf(element, array, pivot, end);
		} else {
			return locationOf(element, array, start, pivot);
		}
	}

	function DecideExtemeTimeRange(currentExtreme, seriesData, direction)
	{
		var dataToCheck = seriesData[0].data;
		var numberOfPoints = dataToCheck.length;
		
		var startTimeOfCurrentExtreme = currentExtreme.min;
		var endTimeofCurrentExtreme = currentExtreme.max;
		
		var allDateTime = dataToCheck.map(function(x){ return x[0]});
        //var startTimeOfAllTime = allDateTime[0];
		//var endTimeOfAllTime = allDateTime[numberOfPoints - 1];

		var startIndex = locationOf(startTimeOfCurrentExtreme, allDateTime);
		var endIndex = locationOf(endTimeofCurrentExtreme, allDateTime);

		if(direction == 'prev')
		{
			if(startIndex == 0)
			{
				return [startTimeOfCurrentExtreme, endTimeofCurrentExtreme];
			}
			else
			{
				return [allDateTime[startIndex - 1], allDateTime[endIndex - 1]];
			}
		}

		if(direction == 'next')
		{
			if(endIndex == numberOfPoints - 1)
			{
				return [startTimeOfCurrentExtreme, endTimeofCurrentExtreme];
			}
			else
			{
				return [allDateTime[startIndex + 1], allDateTime[endIndex + 1]];
			}
			
		}

		alert('You are really fucked up if you reach here...');

	}

	
<<<<<<< HEAD
<<<<<<< HEAD
    GraphGenerator.prototype.GenerateGraph = function(containerSelector, title, seriesData, graphSetUp, numerOfPointToShow = 100) {
		
=======
=======
>>>>>>> 2722c45cb35d410e37d4f8f3d3a780cea6890f36
    GraphGenerator.prototype.GenerateGraph = function(containerSelector, title, seriesData, graphSetUp, numerOfPointToShow = 45, tradeData) {
		for (var i = 0; i < seriesData.length; i++) {
            if (seriesData[i].type == 'ohlc') {
                seriesData[i].events = {
                    click : function(event) {
                        point = event.point;
                        if (tradeData[point.x] == undefined) {
                            tradeData[point.x] = {
                                time: point.x,
                                high: point.high,
                                low: point.low,
                                price: point.high,
                                type: 'long'
                            };
                            this.chart.xAxis[0].addPlotLine({
                                id: '' + point.x,
                                color: 'red',
                                dashStyle: 'solid',
                                width: 3,
                                value: point.x
                            });
                        } else if (tradeData[point.x].type == 'long') {
                            tradeData[point.x].type = 'short';
                            tradeData[point.x].price = tradeData[point.x].low;
                            this.chart.xAxis[0].removePlotLine('' + point.x);
                            this.chart.xAxis[0].addPlotLine({
                                id: '' + point.x,
                                color: 'green',
                                dashStyle: 'solid',
                                width: 3,
                                value: point.x
                            });
                        } else if (tradeData[point.x].type == 'short') {
                            tradeData[point.x] = undefined;
                            this.chart.xAxis[0].removePlotLine('' + point.x);
                        }
                    }
                };
                break;
            }
        }
<<<<<<< HEAD
>>>>>>> add export logic
=======
>>>>>>> 2722c45cb35d410e37d4f8f3d3a780cea6890f36
        $(containerSelector).highcharts('StockChart', {
			chart: {
				events: {
					load: function () {
						this.xAxis[0].setExtremes(
							seriesData[0].data[0][0],
							seriesData[0].data[numerOfPointToShow][0]
						);
					},
					click: function(event) {
					    console.log(this.getSelectedSeries());
					},
				},

			},
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
                    enabled: false
                },
                lineWidth: 2,
                tickInterval: 0.02,
				scalable: false,
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
			exporting: {
				buttons: {					
					nextButton: {
						text: 'Next',
						onclick: function () {							
							var extreme = DecideExtemeTimeRange(this.xAxis[0].getExtremes(), seriesData, 'next');
							this.xAxis[0].setExtremes(
								extreme[0],
								extreme[1]
							);
						},
						symbol: 'circle'
					},
					prevButton: {
						text: 'Prev',
						onclick: function () {							
							var extreme = DecideExtemeTimeRange(this.xAxis[0].getExtremes(), seriesData, 'prev');
							this.xAxis[0].setExtremes(
								extreme[0],
								extreme[1]
							);
						},
						symbol: 'circle'
					},
				}
			},
            series: seriesData
        });
    };
    return GraphGenerator;
}());