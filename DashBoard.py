import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px

# Load CSV file
df = pd.read_csv("top50.csv")

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("NBA Player Stats Dashboard"),
    dcc.Dropdown(
        id='player-dropdown',
        options=[player for player in df['Player'].unique()],
        placeholder="Select a player",
        searchable=True
    ),
    dcc.Graph(id='player-bar-chart'),
    dash_table.DataTable(
        id='player-table',
        columns=[
            {'name': 'Player', 'id': 'Player'},
            {'name': 'Points', 'id': 'Points'},
            {'name': 'Assists', 'id': 'Assists'}
        ],
        style_table={'margin-top': '20px', 'overflowX': 'auto'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
        style_cell={'textAlign': 'center', 'padding': '10px'}
    )
])

@app.callback(
    [Output('player-bar-chart', 'figure'),
     Output('player-table', 'data')],
    [Input('player-dropdown', 'value')]
)
def update_dashboard(selected_player):
    if not selected_player:
        return px.bar(title="Select a player to view stats"), []
    
    filtered_df = df[df['Player'] == selected_player]
    
    fig = px.bar(
        filtered_df.melt(id_vars=['Player'], value_vars=['Points', 'Assists']),
        x='variable',
        y='value',
        text='value',
        title=f"{selected_player}'s Stats",
        labels={'variable': 'Stat', 'value': 'Total'},
        color='variable'
    )
    fig.update_traces(textposition='outside')
    
    return fig, filtered_df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
