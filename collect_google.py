from dataloader import load_data
from plotting import plot_data
from identify_pattern import search

# get pandas dataframe of apple history
google = load_data('GOOGL')

# display top 5 rows
#print(google.iloc[0, 4])

#plot_data(google)
search(google)








