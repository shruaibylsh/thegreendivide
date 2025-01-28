import plotly.express as px
import pandas as pd

walkable = pd.read_csv("walkable_pct.csv")

# Remove any null values first
walkable_clean = walkable.dropna(subset=['pct_walk'])

# Calculate the number of tracts above 50.1%
tracts_above = len(walkable_clean[walkable_clean['pct_walk'] > 50.1])
total_tracts = len(walkable_clean)

# Calculate the percentage
percentage = (tracts_above / total_tracts) * 100

print(f"Total census tracts (excluding null values): {total_tracts}")
print(f"Number of tracts with walkability > 50.1%: {tracts_above}")
print(f"Percentage: {percentage:.2f}%")