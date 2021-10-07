from dataloader import load_data
from plotting import plot_data
from identify_pattern import search

# get pandas dataframe of apple history
apple = load_data('AAPL')

# display top 5 rows
# print(apple.head(5))

engulfing_dates = search('Apple', apple, 'engulfing')
# piercing_dates = search("Apple", apple, 'piercing')

# print(engulfing_dates)
# for i in range(len(piercing_dates)):

#     print(piercing_dates[i])

for i in range(len(engulfing_dates)):

    print(engulfing_dates[i])