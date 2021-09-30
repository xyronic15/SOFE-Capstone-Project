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

    avg = df['Change'].mean()
    bar = go.Bar(x=df['Date'], y=df['Change'])

    fig = go.Figure()
    fig.add_trace(bar)
    fig.add_hline(y=avg, line_dash='dot', annotation_text='Average change after 5 days', annotation_position='bottom right')
    fig.update_layout(xaxis_title="Date", yaxis_title="Change in price after 5 days ()")
    fig.show()


