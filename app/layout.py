from dash.dependencies import Input
from dash import dcc, html
import dash_bootstrap_components as dbc
from utils import generate_metric_card
from constants.generic_constants import COLORS, load_data

df = load_data()

NUMERIC_COLUMNS = df.select_dtypes(include=['number']).columns.tolist()
CATEGORICAL_COLUMNS = df.select_dtypes(
    include=['object', 'category']).columns.tolist()


def create_header():
    """Create the dashboard header section"""
    return dbc.Row([
        dbc.Col([
            html.H1(
                "E-Commerce Analytics Dashboard",
                className="display-4 mb-2",
                style={'color': COLORS['primary'], 'fontWeight': '600'}
            ),
            html.P(
                "Monitor your business performance in real-time",
                className="lead",
                style={'color': '#6C757D', 'fontSize': '1.1rem'}
            )
        ], width=12)
    ], className="mb-4")


def create_action_bar():
    """Create the action buttons section"""
    return dbc.Row([
        dbc.Col([
            dbc.Button(
                [html.I(className="fas fa-file-export me-2"),
                 "Generate Report"],
                id="generate-report-button",
                color="primary",
                size="lg",
                className="shadow-sm w-100",
                style={'borderRadius': '8px', 'padding': '12px 24px'}
            )
        ], width=6),
        dbc.Col([
            dcc.Upload(
                id="upload-data",
                children=dbc.Button(
                    [html.I(className="fas fa-upload me-2"), "Upload Data"],
                    color="secondary",
                    size="lg",
                    className="shadow-sm w-100",
                    style={'borderRadius': '8px', 'padding': '12px 24px'}
                )
            )
        ], width=6)
    ], className="mb-4")


def create_filters():
    """Create the filters section with improved UI/UX"""
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Date Range", className="fw-bold mb-2"),
                    dcc.DatePickerRange(
                        id="date-range",
                        start_date=df["created_at"].min(),
                        end_date=df["created_at"].max(),
                        style={"width": "100%", "padding": "0.5rem",
                               'zIndex': 2,
                               "borderRadius": "8px", }
                    )
                ], xs=12, md=6),
                dbc.Col([
                    html.Label("Order Status", className="fw-bold mb-2"),
                    dcc.Dropdown(
                        id="order-status",
                        options=[
                            {"label": status.title(), "value": status}
                            for status in df["order_status"].unique()
                        ],
                        value=df["order_status"].unique(),
                        multi=True,
                        style={"width": "100%", "padding": "0.5rem",
                               "borderRadius": "8px"}
                    )
                ], xs=12, md=6)
            ])
        ])
    ], className="mb-4 shadow-sm filter-card", style={'borderRadius': '12px', 'border': 'none', 'backgroundColor': 'white'})


def create_metrics():
    """Create the metrics cards section with hover and click effects"""
    return dbc.Row([
        dbc.Col(
            generate_metric_card(
                "total-sales", "Total Sales", "fa-dollar-sign"),
            width=4, className="mb-3"
        ),
        dbc.Col(
            generate_metric_card(
                "total-orders", "Total Orders", "fa-shopping-cart"),
            width=4, className="mb-3"
        ),
        dbc.Col(
            generate_metric_card(
                "avg-order-value", "Avg Order Value", "fa-chart-line"),
            width=4, className="mb-3"
        )
    ], className="mb-4")


def create_chatbot():
    """Create an enhanced chatbot section with improved UI/UX and an under-construction overlay"""
    return dbc.Card(
        [
            html.Div(
                [
                    html.Div(
                        style={
                            'color': 'white',
                            'fontSize': '2rem',
                            # 'fontWeight': 'bold',
                            'textAlign': 'center',
                            'textShadow': '0 2px 4px rgba(0, 0, 0, 0.5)',
                        },
                    )
                ],
                style={
                    'position': 'absolute',
                    'top': 0,
                    'left': 0,
                    'width': '100%',
                    'height': '100%',
                    'backgroundColor': 'rgba(0, 0, 0, 0.10)',
                    'backdropFilter': 'blur(1px)',
                    'zIndex': 1,
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'borderRadius': '16px',
                },
                id="under-construction-overlay",
            ),
            dbc.CardHeader(
                dbc.Row([
                    dbc.Col(html.I(className="fas fa-robot me-2",
                                   style={'color': '#0d6efd'}), width='auto'),
                    dbc.Col(html.H5("Analytics Assistant", className="mb-0"))
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
                    html.Div(
                        id="chat-display",
                        children=[
                            html.Div(
                                dbc.Row([
                                    dbc.Col(
                                        html.I(className="fas fa-robot",
                                               style={'color': '#0d6efd', 'fontSize': '1.2rem'}),
                                        width="auto"
                                    ),
                                    dbc.Col(
                                        "Hello! I'm your analytics assistant. How can I help you analyze your data today?",
                                        style={'paddingLeft': '10px'}
                                    )
                                ], align="center"),
                                className="chat-message bot-message",
                                style={
                                    "padding": "16px",
                                    "borderRadius": "16px",
                                    "backgroundColor": "rgba(13, 110, 253, 0.1)",
                                    "color": "#2c3e50",
                                    "maxWidth": "85%",
                                    "marginBottom": "16px",
                                    "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
                                    "transition": "all 0.3s ease"
                                }
                            )
                        ],
                        style={
                            'height': 'calc(100% - 80px)',
                            'overflowY': 'auto',
                            'backgroundColor': '#ffffff',
                            'borderRadius': '12px',
                            'padding': '20px',
                            'scrollBehavior': 'smooth'
                        }
                    ),
                    html.Div(
                        [
                            dbc.InputGroup(
                                [
                                    dcc.Input(
                                        id="user-input",
                                        type="text",
                                        placeholder="Ask about your data analysis...",
                                        style={
                                            'borderRadius': '25px',
                                            'padding': '12px 25px',
                                            'border': '2px solid rgba(0,0,0,0.1)',
                                            'fontSize': '1rem',
                                            'transition': 'all 0.3s ease',
                                            'flexGrow': 1,
                                            'boxShadow': '0 2px 4px rgba(0,0,0,0.05)'
                                        },
                                        className="form-control"
                                    ),
                                    dbc.Button(
                                        html.I(className="fas fa-paper-plane"),
                                        id="send-button",
                                        color="primary",
                                        style={
                                            'borderRadius': '50%',
                                            'padding': '12px',
                                            'width': '45px',
                                            'height': '45px',
                                            'marginLeft': '10px',
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'justifyContent': 'center',
                                            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                                            'transition': 'all 0.3s ease'
                                        }
                                    ),
                                ],
                                className="mt-3",
                                style={'alignItems': 'center'}
                            )
                        ],
                        style={
                            'marginTop': 'auto',
                            'padding': '0 10px'
                        }
                    )
                ],
                className="d-flex flex-column",
                style={
                    'padding': '20px',
                    'height': '500px',
                    'borderRadius': '0 0 16px 16px'
                }
            ),
        ],
        className="shadow-sm h-100 position-relative",
        style={
            'borderRadius': '16px',
            'border': 'none',
            'backgroundColor': '#ffffff',
            'transition': 'all 0.3s ease',
            'height': '100%'
        }
    )


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


def create_custom_chart_controls():
    """Create the custom chart controls section with enhanced UI/UX."""
    return dbc.Card(
        [
            dbc.CardHeader(
                dbc.Row(
                    [
                        dbc.Col(
                            html.H5("Custom Chart Controls", className="mb-0")
                        ),
                        dbc.Col(
                            dbc.Button(
                                html.I(className="fas fa-undo"),
                                color="link",
                                size="sm",
                                className="text-muted",
                                id="reset-controls",
                                style={'boxShadow': 'none'}
                            ),
                            width="auto",
                        ),
                    ],
                    align="center",
                ),
                style={
                    'backgroundColor': '#ffffff',
                    'borderBottom': '1px solid rgba(0,0,0,0.1)',
                    'padding': '20px',
                    'borderRadius': '16px 16px 0 0'
                },
            ),
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label(
                                        "X-Axis",
                                        className="form-label fw-bold text-muted",
                                    ),
                                    dcc.Dropdown(
                                        id='x-axis-dropdown',
                                        options=[
                                            {'label': col, 'value': col}
                                            for col in df.columns
                                        ],
                                        value=NUMERIC_COLUMNS[0]
                                        if NUMERIC_COLUMNS
                                        else CATEGORICAL_COLUMNS[0],
                                        placeholder="Select a column for X-Axis",
                                        className="chart-dropdown",
                                    ),
                                ],
                                width=6,
                            ),
                            dbc.Col(
                                [
                                    html.Label(
                                        "Y-Axis",
                                        className="form-label fw-bold text-muted",
                                    ),
                                    dcc.Dropdown(
                                        id='y-axis-dropdown',
                                        options=[
                                            {'label': col, 'value': col}
                                            for col in NUMERIC_COLUMNS
                                        ],
                                        value=NUMERIC_COLUMNS[1]
                                        if len(NUMERIC_COLUMNS) > 1
                                        else None,
                                        placeholder="Select a column for Y-Axis",
                                        className="chart-dropdown",
                                    ),
                                ],
                                width=6,
                            ),
                        ],
                        className="mb-4",
                    ),
                    html.Label(
                        "Chart Type", className="form-label fw-bold text-muted"
                    ),
                    dcc.Dropdown(
                        id='chart-type-dropdown',
                        options=[
                            {'label': 'Line Chart', 'value': 'line'},
                            {'label': 'Bar Chart', 'value': 'bar'},
                            {'label': 'Scatter Plot', 'value': 'scatter'},
                        ],
                        value='line',
                        placeholder="Select chart type",
                        className="chart-dropdown mb-4",
                    ),
                    html.Label(
                        "Aggregation", className="form-label fw-bold text-muted"
                    ),
                    dcc.Dropdown(
                        id='aggregation-dropdown',
                        options=[
                            {'label': 'Sum', 'value': 'sum'},
                            {'label': 'Mean', 'value': 'mean'},
                            {'label': 'Median', 'value': 'median'},
                            {'label': 'Count', 'value': 'count'},
                        ],
                        value='sum',
                        placeholder="Select aggregation method",
                        className="chart-dropdown mb-4",
                    ),
                ],
                style={
                    'padding': '20px',
                    'height': '500px',
                },
            ),
        ],
        className="shadow-sm h-100",
        style={
            'borderRadius': '16px',
            'border': 'none',
            'backgroundColor': '#ffffff',
            'transition': 'all 0.3s ease',
        },
    )


def create_action_bar():
    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(html.H4("Dashboard", className="mb-4"), width=12)
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Upload(
                                        id="upload-data",
                                        children=dbc.Button(
                                            [html.I(
                                                className="fas fa-upload me-2"), "Upload Data"],
                                            color="secondary",
                                            size="lg",
                                            className="shadow-sm w-100",
                                            style={'borderRadius': '8px',
                                                   'padding': '12px 24px'}
                                        )
                                    ),
                                    width=6
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        [html.I(
                                            className="fas fa-file-export me-2"), "Generate Report"],
                                        id="generate-report-button",
                                        color="primary",
                                        size="lg",
                                        className="shadow-sm w-100",
                                        style={'borderRadius': '8px',
                                               'padding': '12px 24px'}
                                    ),
                                    width=6
                                )
                            ],
                            className="g-2"
                        ),
                        width=8
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                dbc.Switch(
                                    id="dark-mode-toggle",
                                    label="Dark Mode",
                                    value=False,
                                    disabled=True,
                                    style={
                                        'marginRight': '10px'
                                    }
                                )
                            ],
                            style={
                                'display': 'flex',
                                'alignItems': 'center',
                                'justifyContent': 'flex-end'
                            }
                        ),
                        width="auto",
                        className="ms-auto"
                    )
                ],
                align="center",
                className="mb-4"
            )
        ],
        fluid=True
    )


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
