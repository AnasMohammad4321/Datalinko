import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from layout import layout
from callbacks import register_callbacks

# Initialize Dash app with a modern Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Set the app layout
app.layout = layout

# Register callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True, port=8060)
