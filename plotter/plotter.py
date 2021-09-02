"""
Plotter Class.
"""
import plotly.express as px


class Plotter:
    """

    """
    @staticmethod
    def plotter_scatter(x, y, xlabel=None, ylabel=None):
        fig = px.scatter(x=x, y=y)
        fig.update_layout(
            title="",
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            legend_title="Legend Title",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            )
        )
        fig.show()

    @staticmethod
    def plotter_line(x, y, xlabel=None, ylabel=None):
        fig = px.line(x=x, y=y)
        fig.update_layout(
            title="",
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            legend_title="Legend Title",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            )
        )
        fig.show()