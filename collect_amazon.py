from dataloader import load_data

# get pandas dataframe of apple history
amazon = load_data('AMZN')

# display top 5 rows
print(amazon.head(5))