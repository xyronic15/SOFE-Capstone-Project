import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot


def plot_data(df):
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                        open=df['Open'],
                                        close=df['Close'],
                                        high=df['High'],
                                        low=df['Low'])])

    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.show()


