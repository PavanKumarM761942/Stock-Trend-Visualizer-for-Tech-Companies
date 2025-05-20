# Importing required libraries
import datetime
import yfinance as yf
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Stock Visualization"

# Define a dictionary to map company names to their ticker symbols
company_to_ticker = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Google': 'GOOGL',
    'Amazon': 'AMZN',
    'Facebook': 'META',
    'Tesla': 'TSLA',
    'NVIDIA': 'NVDA',
    'Netflix': 'NFLX',
    'Intel': 'INTC',
    'Adobe': 'ADBE',
    'Alibaba': 'BABA',
    'Cisco': 'CSCO',
    'Disney': 'DIS',
    'IBM': 'IBM',
    'Johnson & Johnson': 'JNJ',
    'McDonald\'s': 'MCD',
    'Nike': 'NKE',
    'Pfizer': 'PFE',
    'Procter & Gamble': 'PG',
    'Visa': 'V',
    'Walmart': 'WMT',
    'Exxon Mobil': 'XOM'
}

# Define the layout of the app using HTML structure
app.layout = html.Div(children=[
    html.H1("Stock Visualization Dashboard", style={'textAlign': 'center'}),
    html.H4("Please enter valid company names (e.g., Apple, Microsoft, Google)", style={'textAlign': 'center'}),
    html.Div([
        dcc.Input(id='input', value='Apple, Microsoft', type='text', style={'width': '400px'}),
        html.Button('Submit', id='submit-button', n_clicks=0)
    ], style={'textAlign': 'center', 'marginBottom': 20}),
    html.Div(id='output-graph')
])

# Define the callback function to update the graph
@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='submit-button', component_property='n_clicks')],
    [dash.dependencies.State('input', 'value')]
)
def update_graph(n_clicks, input_data):
    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime.now()

    # Split input data by comma and strip whitespace
    company_names = [name.strip() for name in input_data.split(',')]

    tickers = []
    data = []

    try:
        for company_name in company_names:
            ticker = company_to_ticker.get(company_name.title())
            if not ticker:
                return html.Div(f"Error: Company name '{company_name}' is invalid")
            tickers.append(ticker)

            # Fetch stock data
            df = yf.download(ticker, start=start, end=end)
            if df.empty:
                return html.Div(f"No data found for {company_name}")

            # Prepare data for graph
            data.append({'x': df.index, 'y': df['Close'], 'type': 'line', 'name': company_name})

        # Create the graph
        graph = dcc.Graph(id="example", figure={
            'data': data,
            'layout': {'title': ', '.join(company_names) + " Stock Data"}
        })

    except Exception as e:
        graph = html.Div(f"Error retrieving stock data: {str(e)}")

    return graph

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
