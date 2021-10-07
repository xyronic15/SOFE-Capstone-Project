import pandas

from dataloader import load_data
from plotting import plot_data
from identify_pattern import search

# get pandas dataframe of apple history
google = load_data('GOOGL')

# plot_data(google)
search('Google', google, 'hammer')
