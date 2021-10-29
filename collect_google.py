import pandas

from dataloader import load_data
from plotting import plot_data
from identify_pattern import search

# get pandas dataframe of apple history
google = load_data('GOOGL')

evening_star_dates = search('Google', google, 'morning_star')

for i in range(len(evening_star_dates)):
    
    print(evening_star_dates[i])
