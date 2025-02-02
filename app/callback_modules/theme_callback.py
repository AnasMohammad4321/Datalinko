from dash import Input, Output, callback, no_update, html, State, ALL, MATCH, ctx
import pandas as pd
import plotly.graph_objects as go
from constants.generic_constants import CHART_TYPES, AGGREGATIONS, LIGHT_THEME, DARK_THEME, load_data
from components.create_graph_with_controls import create_graph_with_controls

def register_theme_callback(app):
    @app.callback(
        Output("main-container", "style"),
        Output("custom-graph", "style"),
        Output("chat-display", "style"),
        [Input("dark-mode-toggle", "value")]
    )
    def toggle_dark_mode(dark_mode):
        theme = DARK_THEME if dark_mode else LIGHT_THEME
        container_style = {
            "backgroundColor": theme["background"],
            "color": theme["text"],
            "padding": "24px",
            "height": "100vh",
        }
        card_style = {
            "backgroundColor": theme["card"],
            "color": theme["text"],
            "border": theme["border"],
            "borderRadius": "16px",
        }
        graph_style = {
            "height": "460px",
            "borderRadius": "12px",
            "backgroundColor": theme["card"],
        }
        return container_style, graph_style, card_style