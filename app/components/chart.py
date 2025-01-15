from dash import dcc, html
import dash_bootstrap_components as dbc

def create_charts():
    """Create enhanced charts section with improved visuals and consistent height"""
    return dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                dbc.Row([
                                    dbc.Col(
                                        html.H5("Sales Trend", className="mb-0")),
                                    dbc.Col(
                                        html.Div([
                                            dbc.Button(
                                                html.I(
                                                    className="fas fa-expand-arrows-alt"),
                                                color="link",
                                                size="sm",
                                                className="text-muted",
                                                style={'boxShadow': 'none'}
                                            ),
                                            dbc.Button(
                                                html.I(
                                                    className="fas fa-download"),
                                                color="link",
                                                size="sm",
                                                className="text-muted ms-2",
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
                            dbc.CardBody(
                                [
                                    dcc.Loading(
                                        id="loading-sales-trend",
                                        children=[
                                            dcc.Graph(
                                                id="sales-trend-chart",
                                                config={
                                                    'displayModeBar': 'hover',
                                                    'scrollZoom': True,
                                                    'displaylogo': False,
                                                    'modeBarButtonsToRemove': [
                                                        'zoomIn2d', 'zoomOut2d', 'lasso2d',
                                                        'select2d', 'toggleSpikelines'
                                                    ]
                                                },
                                                style={
                                                    'height': '380px',
                                                    'borderRadius': '12px'
                                                }
                                            )
                                        ],
                                        type="circle",
                                        color="#0d6efd"
                                    ),
                                    html.Div(
                                        dbc.ButtonGroup(
                                            [
                                                dbc.Button(
                                                    "1D", color="light", size="sm"),
                                                dbc.Button(
                                                    "1W", color="light", size="sm"),
                                                dbc.Button(
                                                    "1M", color="light", size="sm"),
                                                dbc.Button(
                                                    "1Y", color="light", size="sm"),
                                                dbc.Button(
                                                    "ALL", color="light", size="sm"),
                                            ],
                                            size="sm",
                                            className="mt-3"
                                        ),
                                        style={'textAlign': 'center'}
                                    )
                                ],
                                style={
                                    'padding': '20px',
                                    'height': '500px'
                                }
                            )
                        ],
                        className="shadow-sm",
                        style={
                            'borderRadius': '16px',
                            'border': 'none',
                            'backgroundColor': '#ffffff',
                            'height': '100%',
                            'transition': 'all 0.3s ease'
                        }
                    )
                ],
                width=6
            ),
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                dbc.Row([
                                    dbc.Col(
                                        html.H5("Category Sales", className="mb-0")),
                                    dbc.Col(
                                        dbc.ButtonGroup(
                                            [
                                                dbc.Button(
                                                    html.I(
                                                        className="fas fa-chart-pie"),
                                                    color="light",
                                                    size="sm",
                                                    className="active"
                                                ),
                                                dbc.Button(
                                                    html.I(
                                                        className="fas fa-chart-bar"),
                                                    color="light",
                                                    size="sm"
                                                ),
                                            ],
                                            size="sm"
                                        ),
                                        width="auto"
                                    )
                                ], align="center"),
                                style={
                                    'backgroundColor': '#ffffff',
                                    'borderBottom': '1px solid rgba(0,0,0,0.1)',
                                    'padding': '20px',
                                    'borderRadius': '16px 16px 0 0'
                                }
                            ),
                            dbc.CardBody(
                                dcc.Loading(
                                    id="loading-category-sales",
                                    children=[
                                        dcc.Graph(
                                            id="category-sales-chart",
                                            config={
                                                'displayModeBar': 'hover',
                                                'scrollZoom': False,
                                                'displaylogo': False,
                                                'modeBarButtonsToRemove': [
                                                    'zoomIn2d', 'zoomOut2d', 'lasso2d',
                                                    'select2d', 'toggleSpikelines'
                                                ]
                                            },
                                            style={
                                                'height': '380px',
                                                'borderRadius': '12px'
                                            }
                                        )
                                    ],
                                    type="circle",
                                    color="#0d6efd"
                                ),
                                style={
                                    'padding': '20px',
                                    'height': '500px'
                                }
                            )
                        ],
                        className="shadow-sm",
                        style={
                            'borderRadius': '16px',
                            'border': 'none',
                            'backgroundColor': '#ffffff',
                            'height': '100%',
                            'transition': 'all 0.3s ease'
                        }
                    )
                ],
                width=6
            )
        ],
        className="g-4 align-items-stretch"
    )