import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from layout import layout
from callbacks import register_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.layout = layout

register_callbacks(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8060, debug=True)
