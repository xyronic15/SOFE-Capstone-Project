import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
from plotly.subplots import make_subplots


def plot_data(df):
    trace1 = go.Candlestick(x=df['Date'],
                            open=df['Open'],
                            close=df['Close'],
                            high=df['High'],
                            low=df['Low'],
                            name="Candlestick")

    trace2 = go.Scatter(x=df['Date'],
                        y=df['Close'],
                        name="Closing Price")

    fig = go.Figure()
    fig.add_trace(trace1)
    fig.add_trace(trace2)
    fig.update_layout(xaxis_title="Date", yaxis_title="Price ()", xaxis_rangeslider_visible=False)
    fig.show()

def plot_pattern(df):
    trace1 = go.Bar(x=df['Date'], y=['Change'])