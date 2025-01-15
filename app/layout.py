from dash.dependencies import Input
from dash import dcc, html
import dash_bootstrap_components as dbc
from constants.generic_constants import COLORS, load_data
from components.header import create_header
from components.action_bar import create_action_bar
from components.filter import create_filters
from components.metric import create_metrics
from components.chatbot import create_chatbot
from components.chart import create_charts
from components.custom_chart_control import create_custom_chart_controls
df = load_data()

NUMERIC_COLUMNS = df.select_dtypes(include=['number']).columns.tolist()
CATEGORICAL_COLUMNS = df.select_dtypes(
    include=['object', 'category']).columns.tolist()


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
    dbc.Row([
        dbc.Col(create_custom_chart_controls(), width=4, className="h-100"),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(
                    dbc.Row([
                        dbc.Col(
                            html.H5("Custom Visualization", className="mb-0")),
                        dbc.Col(
                            html.Div([
                                dbc.Button(
                                    html.I(
                                        className="fas fa-expand-arrows-alt"),
                                    color="link",
                                    size="sm",
                                    className="text-muted me-2",
                                    style={'boxShadow': 'none'}
                                ),
                                dbc.Button(
                                    html.I(className="fas fa-download"),
                                    color="link",
                                    size="sm",
                                    className="text-muted",
                                    style={'boxShadow': 'none'}
                                )
                            ]),
                            width="auto",
                        )
                    ], align="center"),
                    style={
                        'backgroundColor': '#ffffff',
                        'borderBottom': '1px solid rgba(0,0,0,0.1)',
                        'padding': '20px',
                        'borderRadius': '16px 16px 0 0'
                    }
                ),
                dbc.CardBody([
                    dcc.Loading(
                        id="loading-graph",
                        children=[
                            dcc.Graph(
                                id='custom-graph',
                                style={
                                    'height': '460px',
                                    'borderRadius': '12px'
                                }
                            )
                        ],
                        type="circle",
                        color="#0d6efd"
                    )
                ], style={
                    'padding': '20px',
                    'height': '500px'
                }),
            ],
                className="shadow-sm h-100",
                style={
                'borderRadius': '16px',
                'border': 'none',
                'backgroundColor': '#ffffff',
                'transition': 'all 0.3s ease'
            }),
            width=8,
            className="h-100"
        )
    ], className="align-items-stretch")
], fluid=True, style={"backgroundColor": COLORS['background'], "padding": "24px"})
