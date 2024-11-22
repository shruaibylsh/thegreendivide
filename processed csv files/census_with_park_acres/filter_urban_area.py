import pandas as pd

census = pd.read_csv("census_with_park_acres.csv")

urban_area = census[census['HU_SqM'] > 200]

urban_area.to_csv("urban_area.csv", index = False)