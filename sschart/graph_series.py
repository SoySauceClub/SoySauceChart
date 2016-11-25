class GraphSeries(object):
    def __init__(self, name, headers, seriestype, yAxis=0, style_setup=None):
        self.name = name
        self.headers = headers
        self.seriestype = seriestype
        self.yAxis = yAxis
        self.style_setup = style_setup