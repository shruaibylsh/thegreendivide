import pandas as pd
import numpy as np

census = pd.read_csv("census_with_park_acres.csv")

census_urban = census[census['HU_SqM'] > 200][['park_per1k']]
census_urban.to_csv('census_urban.csv', index=False)

bins = [-np.inf, 0, 4.1, 10, 20, 50, 100, np.inf]
labels = ['0', '0-4.1', '4.1-10', '10-20', '20-50', '50-100', '100+']

# Create categories and count them
census['park_per1k'] = pd.cut(census['park_per1k'], bins=bins, labels=labels)
park_per1k_hist = census['park_per1k'].value_counts().reset_index()
park_per1k_hist.columns = ['park_per1k_range', 'count']

# Sort by the natural order of ranges
park_per1k_hist['sort_order'] = pd.Categorical(park_per1k_hist['park_per1k_range'], 
                                             categories=labels, 
                                             ordered=True)
park_per1k_hist = park_per1k_hist.sort_values('sort_order')
park_per1k_hist = park_per1k_hist[['park_per1k_range', 'count']]

# Save the category counts
park_per1k_hist.to_csv('park_per1k_hist.csv', index=False)

