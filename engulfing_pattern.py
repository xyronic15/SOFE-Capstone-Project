import pandas as pd
from dataloader import load_data, load_all
# from plotting import plot_data
from identify_pattern import search

# get pandas dataframe of all companies stock history
apple, google, amazon, tesla = load_all()

# get all info on engulfing candlesticks
# apple_eng = search(apple, "engulfing")
# google_eng = search(google, "engulfing")
# amazon_eng = search(amazon, "engulfing")
# tesla_eng = search(tesla, "engulfing")

# Proof of concept data
apple_eng = apple[['Date', 'Close']].head(5)
google_eng = google[['Date', 'Close']].head(5)
amazon_eng = amazon[['Date', 'Close']].head(5)
tesla_eng = tesla[['Date', 'Close']].head(5)
companies = [apple_eng, google_eng, amazon_eng, tesla_eng]

df = pd.DataFrame(columns = ['Date', 'Close'])

for company in companies:

    df = pd.concat([df, company])

print(df)
df.to_csv('engulfing_pattern.csv')
