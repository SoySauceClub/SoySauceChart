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
	
    GraphGenerator.prototype.GenerateGraph = function(containerSelector, title, seriesData, graphSetUp, numerOfPointToShow = 10) {
		
        $(containerSelector).highcharts('StockChart', {
			chart: {
				events: {
					load: function () {
						this.xAxis[0].setExtremes(
							seriesData[0].data[0][0],
							seriesData[0].data[numerOfPointToShow][0]
						);
					}
				}
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
                    enabled: true
                },
                lineWidth: 2,
                tickInterval: 0.02,
				scalable: true,
				opposite:false
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