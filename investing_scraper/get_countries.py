import pandas as pd
df = pd.read_csv("holidays_data.csv")
countries = sorted(df['Country'].dropna().unique().tolist())
print(countries)
