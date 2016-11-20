class GraphSeries(object):
    def __init__(self, name, headers, seriestype, yAxis=0):
        self.name = name
        self.headers = headers
        self.seriestype = seriestype
        self.yAxis = yAxis