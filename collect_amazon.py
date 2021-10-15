from dataloader import load_data
from identify_pattern import search

# get pandas dataframe of apple history
amazon = load_data('AMZN')


evening_star_dates = search('Amazon', amazon, 'three_black_crows')

for i in range(len(evening_star_dates)):
    
    print(evening_star_dates[i])