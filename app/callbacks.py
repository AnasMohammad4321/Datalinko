from dash import Input, Output, callback, no_update, html, State, ALL, MATCH, ctx
import pandas as pd
import plotly.graph_objects as go
from constants.generic_constants import CHART_TYPES, AGGREGATIONS, LIGHT_THEME, DARK_THEME, load_data
from components.create_graph_with_controls import create_graph_with_controls

from callback_modules.theme_callback import register_theme_callback
from callback_modules.dashboard_callback import register_dashboard_callback
from callback_modules.graph_management_callback import register_graph_management_callback
from callback_modules.axis_options_callback import register_axis_options_callback
from callback_modules.graph_update_callback import register_graph_update_callback
from callback_modules.chat_callback import register_chat_callback

df = load_data()

NUMERIC_COLUMNS = df.select_dtypes(include=['number']).columns.tolist()
CATEGORICAL_COLUMNS = df.select_dtypes(include=['object', 'category']).columns.tolist()

def register_callbacks(app):
    register_theme_callback(app)
    register_dashboard_callback(app)
    register_graph_management_callback(app)
    register_axis_options_callback(app)
    register_graph_update_callback(app)
    register_chat_callback(app)