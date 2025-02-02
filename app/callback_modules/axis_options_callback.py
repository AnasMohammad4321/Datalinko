from dash import Input, Output, callback, no_update, html, State, ALL, MATCH, ctx
import pandas as pd
import plotly.graph_objects as go
from constants.generic_constants import CHART_TYPES, AGGREGATIONS, LIGHT_THEME, DARK_THEME, load_data
from components.create_graph_with_controls import create_graph_with_controls

df = load_data()

NUMERIC_COLUMNS = df.select_dtypes(include=['number']).columns.tolist()
CATEGORICAL_COLUMNS = df.select_dtypes(include=['object', 'category']).columns.tolist()

def register_axis_options_callback(app):
    @app.callback(
        Output({'type': 'y-axis-dropdown', 'index': MATCH}, 'options'),
        Input({'type': 'x-axis-dropdown', 'index': MATCH}, 'value')
    )
    def update_yaxis_options(selected_x):
        if selected_x in NUMERIC_COLUMNS:
            return [{'label': col, 'value': col} for col in NUMERIC_COLUMNS]
        return [{'label': col, 'value': col}
                for col in NUMERIC_COLUMNS if col != selected_x]