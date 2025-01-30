from dash.dependencies import Input, Output, State
from dash import dcc, html
import dash_bootstrap_components as dbc
from datetime import datetime
from app.constants.generic_constants import COLORS, load_data
from app.components.header import create_header
from app.components.action_bar import create_action_bar
from app.components.filter import create_filters
from app.components.metric import create_metrics
from app.components.chatbot import create_chatbot
from app.components.chart import create_charts
from app.components.create_graph_with_controls import create_graph_with_controls
from app.components.footer import create_footer
df = load_data()

NUMERIC_COLUMNS = df.select_dtypes(include=['number']).columns.tolist()
CATEGORICAL_COLUMNS = df.select_dtypes(
    include=['object', 'category']).columns.tolist()

FIRST_GRAPH_ID = 1

layout = dbc.Container([
    create_header(),
    create_action_bar(),
    create_filters(),
    create_metrics(),
    dbc.Row(
        [
            dbc.Col(
                create_chatbot(),
                width=4,
                className="h-100"
            ),
            dbc.Col(
                create_charts(),
                width=8,
                className="h-100"
            )
        ],
        className="mb-4 align-items-stretch"
    ),
    dbc.Button(
        [html.I(className="fas fa-plus me-2"), "Add Custom Graph"],
        id="add-graph-button",
        color="primary",
        className="mb-4 shadow-sm",
        style={
            'borderRadius': '8px',
            'padding': '12px 24px',
            'fontWeight': '500',
            'backgroundColor': COLORS['primary']
        }
    ),
    html.Div(
        id='graphs-container',
        children=[create_graph_with_controls(id_suffix=FIRST_GRAPH_ID)],
        className="custom-graphs-container"
    ),
    create_footer()
], fluid=True, style={
    "backgroundColor": COLORS['background'],
    "padding": "24px",
    "minHeight": "100vh",
    "borderRadius": "16px",
    "boxShadow": "0 0 20px rgba(0,0,0,0.05)"
})
