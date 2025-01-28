import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

walkable = pd.read_csv("walkable_pct.csv")

# Calculate stats for income groups
walkable_clean = walkable.dropna(subset=['pct_walk'])
median_income = walkable_clean['Med_HH_Inc'].median()
walkable_clean['income_category'] = pd.cut(walkable_clean['Med_HH_Inc'],
    bins=[-np.inf, 0.8*median_income, 1.2*median_income, np.inf],
    labels=['Low Income', 'Middle Income', 'High Income'])
income_stats = walkable_clean.groupby('income_category')['pct_walk'].mean().round(2)

# Calculate percentage with access for each racial/ethnic group
def calc_group_access(pop_pct_col):
    group_pop = walkable_clean['Pop_20'] * walkable_clean[pop_pct_col] / 100
    group_pop_with_access = group_pop * walkable_clean['pct_walk'] / 100
    return (group_pop_with_access.sum() / group_pop.sum() * 100).round(1)

race_stats = pd.Series({
    'White (non-Hispanic)': calc_group_access('PC_NH_wht'),
    'Black (non-Hispanic)': calc_group_access('PC_NH_Blk'),
    'Asian (non-Hispanic)': calc_group_access('PC_NH_Asn'),
    'Hispanic': calc_group_access('PC_Hispani')
})

# Create subplots
fig = make_subplots(
    rows=2, 
    cols=1,
    vertical_spacing=0.1,  # Reduced spacing
    subplot_titles=('By Income (%)', 'By Race/Ethnicity (%)'),
    row_heights=[0.3, 0.4]
)

# Add income bars
fig.add_trace(
    go.Bar(
        x=income_stats.values,
        y=income_stats.index,
        orientation='h',
        text=[f"{val:.0f}" for val in income_stats.values],
        textposition='auto',
        marker_color='#75b765',
        marker=dict(line=dict(width=0)),
        name='Income'
    ),
    row=1, col=1
)

# Add race/ethnicity bars
fig.add_trace(
    go.Bar(
        x=race_stats.values,
        y=race_stats.index,
        orientation='h',
        text=[f"{val:.0f}" for val in race_stats.values],
        textposition='auto',
        marker_color='#7fdbda',
        marker=dict(line=dict(width=0)),
        name='Race/Ethnicity'
    ),
    row=2, col=1
)

# Update layout
fig.update_layout(
    showlegend=False,
    height=500,
    width=800,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=180, r=20, t=60, b=20),
    bargap=0.4
)

# Update axes
for i in [1, 2]:
    fig.update_xaxes(
        range=[0, 100],
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        row=i, col=1
    )
    fig.update_yaxes(
        autorange="reversed",
        showgrid=True,
        gridcolor='rgba(0,0,0,0.1)',
        gridwidth=1,
        tickfont=dict(size=14),
        row=i, col=1
    )

# Update subplot titles
fig.update_annotations(font_size=24, x=0, xanchor='left')

# Save as HTML
fig.write_html("walkability_by_demographics2.html")

# Also display the plot
fig.show()