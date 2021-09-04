"""
Plotter Class.
"""
import plotly.express as px
import plotly.graph_objects as go

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
    def plotter_line(x, y, xlabel=None, ylabel=None, names=None):
        if names:
            fig = go.Figure()
            for i in range(len(names)):
                fig.add_trace(go.Scatter(
                    x=x,
                    y=y[i],
                    name=names[i] # this sets its legend entry
                ))
            fig.update_layout(
                title="",
                xaxis_title=xlabel,
                yaxis_title=ylabel,
                legend_title="Legenda",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="RebeccaPurple"
                )
            )
            fig.show()
        else:
            fig = px.line(x=x, y=y, labels=names)
            fig.update_layout(
                title="",
                xaxis_title=xlabel,
                yaxis_title=ylabel,
                legend_title="Legenda",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="RebeccaPurple"
                )
            )
            fig.show()