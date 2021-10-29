from dataloader import load_data
from identify_pattern import search

# get pandas dataframe of apple history
tesla = load_data('TSLA')

dark_cloud_dates = search('Tesla', tesla, 'dark_cloud_cover')

for i in range(len(dark_cloud_dates)):
    
    print(dark_cloud_dates[i])