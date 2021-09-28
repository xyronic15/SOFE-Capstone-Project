from dataloader import load_data

# get pandas dataframe of apple history
google = load_data('GOOGL')

# display top 5 rows
print(google.head(5))