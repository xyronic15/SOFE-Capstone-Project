from dataloader import load_data
from identify_pattern import search

# get pandas dataframe of apple history
amazon = load_data('AMZN')


rising_dates = search('Amazon', amazon, 'rising_three_methods')

for i in range(len(rising_dates)):
    
    print(rising_dates[i])