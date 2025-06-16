import pandas as pd
from flask import Flask, render_template, request
import plotly.express as px
import plotly.io as pio
import numpy as np
import re

app = Flask(__name__)

# Load inventory data
inventory_df = pd.read_csv('static/inventory.csv')
inventory_df['createdAt'] = pd.to_datetime(inventory_df['createdAt'], format='%d-%m-%Y')

# Function to clean non-numeric values
def clean_numeric_value(value):
    try:
        # Remove any non-numeric characters except for periods
        value = re.sub(r'[^\d.]', '', str(value))
        # Convert empty strings to NaN
        if value == '':
            return np.nan
        return float(value)
    except ValueError:
        return np.nan  # Handle non-convertible values with NaN

# Clean 'stock' column
inventory_df['stock_clean'] = inventory_df['stock'].apply(clean_numeric_value)

# Clean 'priceWithGST' column
inventory_df['priceWithGST_clean'] = inventory_df['priceWithGST'].apply(clean_numeric_value)

# Drop rows where 'stock_clean' or 'priceWithGST_clean' is NaN (optional)
inventory_df = inventory_df.dropna(subset=['stock_clean', 'priceWithGST_clean'])

@app.route('/', methods=['GET', 'POST'])
def index():
    graph_stock = None
    graph_avg_price = None
    graph_totals = None
    table = None

    if request.method == 'POST':
        company_name = request.form.get('companyName')
        month = request.form.get('month')
        year = request.form.get('year')

        # Filter data based on user selection
        filtered_df = inventory_df[
            (inventory_df['companyName'] == company_name) &
            (inventory_df['createdAt'].dt.month == int(month)) &
            (inventory_df['createdAt'].dt.year == int(year))
        ]

        # Calculate average and total stock and price
        avg_stock = filtered_df['stock_clean'].mean(skipna=True)  # skipna=True to ignore NaN values
        total_stock = filtered_df['stock_clean'].sum(skipna=True)
        avg_price = filtered_df['priceWithGST_clean'].mean(skipna=True)
        total_price = filtered_df['priceWithGST_clean'].sum(skipna=True)

        # Plot graph: Stock by Product
        fig_stock = px.bar(filtered_df, x='productName', y='stock_clean', title='Stock by Product')
        graph_stock = pio.to_html(fig_stock, full_html=False)

        # Plot graph: Average Price by Product
        fig_avg_price = px.bar(filtered_df, x='productName', y='priceWithGST_clean', title='Average Price by Product')
        graph_avg_price = pio.to_html(fig_avg_price, full_html=False)

        # Calculate total stock and total price by product
        total_data = filtered_df.groupby('productName').agg({
            'stock_clean': 'sum',
            'priceWithGST_clean': 'sum'
        }).reset_index()

        # Plot graph: Total Stock and Total Price by Product
        fig_totals = px.bar(total_data, x='productName', y=['stock_clean', 'priceWithGST_clean'],
                            title='Total Stock and Total Price by Product', barmode='stack')
        graph_totals = pio.to_html(fig_totals, full_html=False)

        # Prepare table data
        table_data = f"""
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Statistic</th>
                        <th>Value</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>Total Stock</td><td>{total_stock}</td></tr>
                    <tr><td>Average Stock</td><td>{avg_stock:.2f}</td></tr>
                    <tr><td>Total Price</td><td>{total_price}</td></tr>
                    <tr><td>Average Price</td><td>{avg_price:.2f}</td></tr>
                </tbody>
            </table>
        """

        table = table_data

    # Get unique company names for the dropdown
    companies = inventory_df['companyName'].unique()

    # Get unique months and years present in the data
    months = sorted(inventory_df['createdAt'].dt.month.unique())
    years = sorted(inventory_df['createdAt'].dt.year.unique())

    return render_template('index.html', companies=companies, months=months, years=years,
                           graph_stock=graph_stock, graph_avg_price=graph_avg_price, graph_totals=graph_totals,
                           table=table)

if __name__ == '__main__':
    app.run(debug=True)
