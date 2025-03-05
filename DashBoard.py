import dash
from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd

# Sample dataset
df = pd.DataFrame({
    "Category": ["LeBron", "LeBron", "Michael Jordan", "Michael Jordan", "Kobe Bryant", "Kobe Bryant"],
    "Value": [41871, 11487, 32292, 5633, 33643, 6306],
    "Subcategory": ["PTS", "AST", "PTS", "AST", "PTS", "AST"]
})

# Initialize Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Who is the 'GOAT'?", style={'textAlign': 'center'}),

    dcc.Dropdown(
        id="category-dropdown",
        options=[{"label": cat, "value": cat} for cat in df["Category"].unique()],
        value="A",
        clearable=False
    ),

    dcc.Graph(id="bar-chart"),

    dash_table.DataTable(
        id="data-table",
        columns=[{"name": col, "id": col} for col in df.columns],
        page_size=5
    )
])

# Callback to update graph and table
@app.callback(
    [dash.Output("bar-chart", "figure"),
     dash.Output("data-table", "data")],
    [dash.Input("category-dropdown", "value")]
)
def update_dashboard(selected_category):
    filtered_df = df[df["Category"] == selected_category]
    fig = px.bar(filtered_df, x="Subcategory", y="Value", title=f"Values for Category {selected_category}")
    return fig, filtered_df.to_dict("records")

# Run server
if __name__ == "__main__":
    app.run_server(debug=True)
