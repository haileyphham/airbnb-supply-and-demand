import numpy as np
import pandas as pd
import plotly.graph_objects as go
import os

# Load the data
boston = pd.read_csv("airbnb.csv")

# Analysis
boston_q1_1 = boston[boston['room_type'] == "Entire home/apt"]
boston_q1_2 = boston_q1_1[boston_q1_1['dow'].between(4, 6)]
boston_q1_3 = boston_q1_2[boston_q1_2['price'] < 1000]

boston_pre = boston_q1_3[boston_q1_3['month'] <= 6]
boston_post = boston[boston['month'] > 6]

# Pre-tax demand
boston_pre_demand = boston_pre[boston_pre['master_key'] == 2]
bins = np.arange(0, 1001, 20)
boston_pre_demand_binned = pd.cut(boston_pre_demand['price'], bins=bins)
boston_pre_demand_binned_counts = boston_pre_demand_binned.value_counts().sort_index()

boston_pre_demand_binned_df = pd.DataFrame({
    'price': [interval.left for interval in boston_pre_demand_binned_counts.index],  
    'quantity': boston_pre_demand_binned_counts.values
})
boston_pre_demand_binned_df['quantity_demanded'] = boston_pre_demand_binned_df['quantity'][::-1].cumsum()[::-1]

# Pre-tax supply
boston_pre_supply_binned = pd.cut(boston_pre['price'], bins=bins)
boston_pre_supply_binned_counts = boston_pre_supply_binned.value_counts().sort_index()

boston_pre_supply_binned_df = pd.DataFrame({
    'price': [interval.left for interval in boston_pre_supply_binned_counts.index], 
    'quantity': boston_pre_supply_binned_counts.values
})
boston_pre_supply_binned_df['quantity_supplied'] = boston_pre_supply_binned_df['quantity'].cumsum()

# Post-tax demand
boston_post_filtered = boston_post[(boston_post['room_type'] == "Entire home/apt") & (boston_post['dow'].between(4, 5))]
boston_post_demand = boston_post_filtered[boston_post_filtered['master_key'] == 2]
boston_post_demand_binned = pd.cut(boston_post_demand['price'], bins=bins)
boston_post_demand_binned_counts = boston_post_demand_binned.value_counts().sort_index()

boston_post_demand_binned_df = pd.DataFrame({
    'price': [interval.left for interval in boston_post_demand_binned_counts.index],  
    'quantity': boston_post_demand_binned_counts.values
})
boston_post_demand_binned_df['quantity_demanded'] = boston_post_demand_binned_df['quantity'][::-1].cumsum()[::-1]

# generate html files per plot
def plot_demand_curve():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=boston_pre_demand_binned_df['quantity_demanded'], 
                             y=boston_pre_demand_binned_df['price'], 
                             mode='lines', 
                             name='Demand Curve'))
    fig.update_layout(title="Demand Curve", xaxis_title="Quantity", yaxis_title="Price")
    fig.write_html('charts/demand_curve.html')

def plot_supply_curve():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=boston_pre_supply_binned_df['quantity_supplied'], 
                             y=boston_pre_supply_binned_df['price'], 
                             mode='lines', 
                             name='Supply Curve'))
    fig.update_layout(title="Supply Curve", xaxis_title="Quantity", yaxis_title="Price")
    fig.write_html('charts/supply_curve.html')

def plot_supply_demand_curves():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=boston_pre_demand_binned_df['quantity_demanded'], 
                             y=boston_pre_demand_binned_df['price'], 
                             mode='lines', 
                             name='Demand Curve', 
                             line=dict(color='red')))
    fig.add_trace(go.Scatter(x=boston_pre_supply_binned_df['quantity_supplied'], 
                             y=boston_pre_supply_binned_df['price'], 
                             mode='lines', 
                             name='Supply Curve'))
    fig.update_layout(title="Supply and Demand Curves", xaxis_title="Quantity", yaxis_title="Price")
    fig.write_html('charts/supply_demand.html')

def plot_tax_effect():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=boston_pre_demand_binned_df['quantity_demanded'], 
                             y=boston_pre_demand_binned_df['price'], 
                             mode='lines', 
                             name="Pre-tax Demand"))
    fig.add_trace(go.Scatter(x=boston_post_demand_binned_df['quantity_demanded'], 
                             y=boston_post_demand_binned_df['price'], 
                             mode='lines', 
                             name="Post-tax Demand"))
    fig.add_trace(go.Scatter(x=boston_pre_supply_binned_df['quantity_supplied'], 
                             y=boston_post_demand_binned_df['price'], 
                             mode='lines', 
                             name="Supply"))
    fig.update_layout(title="Effect of Tax on Supply and Demand", xaxis_title="Quantity", yaxis_title="Price")
    fig.write_html('charts/tax_effect.html')

#generate html files
plot_demand_curve()
plot_supply_curve()
plot_supply_demand_curves()
plot_tax_effect()


html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Airbnb Supply and Demand Analysis</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #2c3e50;
            color: #ecf0f1;
            padding: 20px;
        }}
        h1 {{
            text-align: center;
            color: #ecf0f1;
        }}
        .chart {{
            margin: 20px 0;
        }}
        .chart h2 {{
            color: #ecf0f1;
        }}
    </style>
</head>
<body>
    <h1>Airbnb Supply and Demand Analysis</h1>
    
    <div class="chart">
        <h2>Demand Curve (Pre-Tax)</h2>
        <iframe src="charts/demand_curve.html" width="100%" height="600px"></iframe>
    </div>
    
    <div class="chart">
        <h2>Supply Curve</h2>
        <iframe src="charts/supply_curve.html" width="100%" height="600px"></iframe>
    </div>

    <div class="chart">
        <h2>Supply and Demand Curves</h2>
        <iframe src="charts/supply_demand.html" width="100%" height="600px"></iframe>
    </div>

    <div class="chart">
        <h2>Effect of Tax on Supply and Demand</h2>
        <iframe src="charts/tax_effect.html" width="100%" height="600px"></iframe>
    </div>
</body>
</html>
"""

with open("index.html", "w") as file:
    file.write(html_content)

print("Static HTML file generated: index.html")
