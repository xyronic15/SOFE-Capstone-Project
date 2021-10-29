from dataloader import load_data
from plotting import plot_data
from identify_pattern import search

# get pandas dataframe of apple history
apple = load_data('AAPL')

# display top 5 rows
# print(apple.head(5))

evening_star_dates = search('Apple', apple, 'doji')

for i in range(len(evening_star_dates)):
    
    print(evening_star_dates[i])