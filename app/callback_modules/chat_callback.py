from dash import Input, Output, callback, no_update, html, State, ALL, MATCH, ctx
import pandas as pd
import plotly.graph_objects as go
from constants.generic_constants import CHART_TYPES, AGGREGATIONS, LIGHT_THEME, DARK_THEME, load_data
from components.create_graph_with_controls import create_graph_with_controls

def register_chat_callback(app):
    @app.callback(
        Output("chat-display", "children"),
        [Input("send-button", "n_clicks"),
         Input("user-input", "value")]
    )
    def update_chat(n_clicks, user_input):
        if not n_clicks or not user_input:
            return no_update

        return [
            html.Div(
                user_input,
                className="chat-message user-message",
                style={
                    "backgroundColor": "#18BC9C",
                    "color": "white",
                    "padding": "12px",
                    "borderRadius": "15px",
                    "marginBottom": "8px",
                    "maxWidth": "80%",
                    "marginLeft": "auto"
                }
            )
        ]
