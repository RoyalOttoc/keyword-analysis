import pandas as pd

df = pd.read_excel('./URLS/urls.xlsx')
print(df["URL"][0])
