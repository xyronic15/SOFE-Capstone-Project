from dataloader import load_data
from plotting import plot_data
from identify_pattern import search

# get pandas dataframe of apple history
apple = load_data('AAPL')

# display top 5 rows
# print(apple.head(5))

search(apple)