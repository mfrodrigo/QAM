"""
Plotter Class.
"""
import plotly.express as px


class Plotter:
    """

    """
    @staticmethod
    def plotter_scatter(x, y):
        fig = px.scatter(x=x, y=y)
        fig.show()

    @staticmethod
    def plotter_line(x, y):
        fig = px.line(x=x, y=y)
        fig.show()