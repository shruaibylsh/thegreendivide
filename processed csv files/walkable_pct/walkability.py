import plotly.express as px
import pandas as pd

walkable = pd.read_csv("walkable_pct.csv")

import numpy as np
import plotly.graph_objects as go

# Remove any null values
walkable_clean = walkable.dropna(subset=['pct_walk'])

# Calculate the bin edges and centers
bin_edges = np.linspace(0, 100, 41)  # 40 bins means 41 edges
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

# Create histogram values manually
hist, _ = np.histogram(walkable_clean['pct_walk'], bins=bin_edges)

# Create colors for each bin
colors = ['#d4eeed' if x < 13 else 
         '#5871a1' if x > 87 else 
         f'rgba({int(212 + (88-212)*(x-13)/(87-13))}, {int(238 + (113-238)*(x-13)/(87-13))}, {int(237 + (161-237)*(x-13)/(87-13))}, 1)'
         for x in bin_centers]

# Create the figure
fig = go.Figure(go.Bar(
    x=bin_centers,
    y=hist,
    width=(bin_edges[1] - bin_edges[0]),  # Width of each bar
    marker_color=colors
))

# Update the layout
fig.update_layout(
    title='Distribution of Walkable Area Percentages',
    xaxis_title='Percentage of Walkable Area',
    yaxis_title='Count',
    showlegend=False,
    bargap=0,  # Remove gaps between bars
    xaxis=dict(
        range=[0, 100],
        tickmode='linear',
        dtick=10
    )
)

# Save the plot as PNG with good resolution
fig.write_image("walkable_histogram.png", width=1200, height=800, scale=2)

# Show the plot
fig.write_html("walkable_histogram.html", full_html=True)