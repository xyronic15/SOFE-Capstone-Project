from dataloader import load_data
from plotting import plot_data
from identify_pattern import search

# get pandas dataframe of apple history
apple = load_data('AAPL')

# display top 5 rows
# print(apple.head(5))

# engulfing_dates = search(apple)
piercing_dates = search("Apple", apple, 'piercing')

# print(engulfing_dates)
print(piercing_dates)