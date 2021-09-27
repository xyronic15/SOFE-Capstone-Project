from dataloader import load_data

# get pandas dataframe of apple history
apple = load_data('AAPL')

# display top 5 rows
print(apple.head(5))