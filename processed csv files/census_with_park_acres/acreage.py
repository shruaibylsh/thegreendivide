import plotly.express as px
import pandas as pd

park_acreage = pd.read_csv("census_urban.csv")

# divide data into several categories
bins = [-1, 0, 1, 3, 4.1, 10, float('inf')]
labels = ['0', '0-1', '1-3', '3-4.1', '4.1-10', '>10']
park_acreage['category'] = pd.cut(park_acreage['park_per1k'], bins=bins, labels=labels)

# Count areas in each category
category_counts = park_acreage['category'].value_counts().reset_index()
category_counts.columns = ['category', 'number of tracts']

# create pie chart
custom_colors = ["#e3f1d2", "#cbe0b2", "#b2d2b4", "#99c5b6", "#6fa9aa", "#4d8c8c"]

fig = px.pie(
    category_counts,
    names='category',
    values='number of tracts',
    color_discrete_sequence=custom_colors,
    category_orders={'category': labels}  # Ensure order matches bins/labels
)

fig.show()
fig.write_html("park_acres_pie_chart.html", full_html=True)