'''
This script compares the pattern dates found in the CSV files in the collected and identified folders
and displays graphs comparing them.
'''

import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
from plotly.subplots import make_subplots

def compare_data(pattern):
    '''
    This function reads the CSV files in the collected and identified folders with corresponding pattern name.
    It converts them into dataframes and performas an innermerge to gain the intersection.
    Then it compares the resultant dataframe with the one generated from the collected folder to receive the percentage of successful identifications.
    '''

    # read the CSV files
    actual_dates = pd.read_csv("./collected/" + pattern + ".csv")
    identified_dates = pd.read_csv("./identified/" + pattern + ".csv")

    # get the intersection dataframe
    intersection = pd.merge(actual_dates, identified_dates[['Name', 'Date']],how='inner')
    
    # get percentage of successful identifications and count of extra identifications
    success_percent = (len(intersection) / len(actual_dates)) * 100
    extra_count = len(identified_dates) - len(intersection)

    # return a dictionary with the percentage and extra count
    data = []
    data.append({'Name': pattern, 'Success': success_percent, 'Actual Total': len(actual_dates), 'Extra': extra_count})
    return data

def plot_info(df):
    '''
    Take the dataframe containing Name, Success%, and Extra.
    Plot the success rate of our identification functions on one bar chart and the count of extra dates on another
    '''
    # Make the subplots
    subplot = make_subplots(rows=1, cols=3, specs=[[{"type":"xy"}, {"type":"xy"}, {"type": "xy"}]],
        subplot_titles=("Percentage of Successful Identifications of Each Pattern", "Frequency of Extra Dates Identified for Each Pattern", "Total Number of Actual Dates"))

    # success percentage bar chart
    subplot.add_bar(row=1, col=1, y=df['Success'], x=df['Name'], name="")

    # extra dates count bar chart
    subplot.add_bar(row=1, col=2, y=df['Extra'], x=df['Name'], name="")

    # total for actual dates bar chart
    subplot.add_bar(row=1, col=3, y=df['Actual Total'], x=df['Name'], name="")

    # show the results
    subplot.update_layout(showlegend=False)
    subplot['layout']['xaxis']['title']='Candlestick Pattern'
    subplot['layout']['xaxis2']['title']='Candlestick Pattern'
    subplot['layout']['xaxis3']['title']='Candlestick Pattern'
    subplot['layout']['yaxis']['title']='Success Percentage (%)'
    subplot['layout']['yaxis2']['title']='Frequency'
    subplot['layout']['yaxis3']['title']='Frequency'
    subplot.show()
    

def main():

    # patterns = ['hammer', 'inv_hammer', 'engulfing_bullish', 'piercing', 'morning_star', 'three_white_soldiers', 'rising_three_methods',
    #     'evening_star', 'three_black_crows', 'shooting_star', 'bearish_engulfing', 'doji', 'hanging_man', 'dark_cloud_cover', 'falling_three_methods']
    patterns = ['engulfing_bullish', 'piercing', 'evening_star']
    data = []

    for pattern in patterns:
        data.extend(compare_data(pattern))
    df = pd.DataFrame(data)

    plot_info(df)
    
    

if __name__ == '__main__':
    main()
    