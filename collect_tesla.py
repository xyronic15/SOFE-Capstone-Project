from dataloader import load_data
from identify_pattern import search

# get pandas dataframe of apple history
tesla = load_data('TSLA')

# display top 5 rows
print(tesla.head(5))
search('Tesla', tesla, 'hammer')