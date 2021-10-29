from dataloader import load_data
from identify_pattern import search

# get pandas dataframe of apple history
tesla = load_data('TSLA')

falling3_dates = search('Tesla', tesla, 'falling_three_methods')

for i in range(len(falling3_dates)):
    
    print(falling3_dates[i])