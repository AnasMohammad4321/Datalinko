from dash import dcc, html
import dash_bootstrap_components as dbc
from constants.generic_constants import COLORS


def create_header():
    """Create the dashboard header section"""
    return dbc.Row([
        dbc.Col([
            html.H1(
                "DataLinko",
                className="display-4 mb-2",
                style={'color': COLORS['primary'], 'fontWeight': '600'}
            ),
            html.P(
                "Monitor your business performance in real-time with DataLinko",
                className="lead",
                style={'color': '#6C757D', 'fontSize': '1.1rem'}
            )
        ], width=12)
    ], className="mb-4")
