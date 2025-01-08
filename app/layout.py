from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from utils import generate_metric_card

# Load and preprocess data
df = pd.read_csv("./data/raw/sample_data.csv", low_memory=False)
df["created_at"] = pd.to_datetime(df["created_at"])

# Enhanced color palette
COLORS = {
    'primary': '#2C3E50',
    'secondary': '#18BC9C',
    'background': '#F8F9FA',
    'text': '#2C3E50',
    'chatbot': {
        'background': '#F8F9FA',
        'user_message': '#18BC9C',
        'bot_message': '#EBF5FB',
        'user_text': '#FFFFFF',
        'bot_text': '#2C3E50',
    },
    'border': '#E9ECEF',
    'hover': '#F1F2F6',
    'chart_colors': ['#18BC9C', '#3498DB', '#E74C3C', '#F39C12', '#9B59B6']
}

# Data column classifications
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
                               "borderRadius": "8px"}
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
    """Create the enhanced chatbot section"""
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H5("Analytics Assistant", className="mb-0"),
                style={
                    'backgroundColor': '#f8f9fa',
                    'borderBottom': '1px solid #dee2e6',
                    'padding': '16px',
                    'borderRadius': '12px 12px 0 0'
                }
            ),
            dbc.CardBody(
                [
                    # Chat display area
                    html.Div(
                        id="chat-display",
                        children=[
                            html.Div(
                                html.Div([
                                    html.I(className="fas fa-robot me-2"),
                                    "Hello! How can I assist you today?"
                                ], style={'display': 'flex', 'alignItems': 'center'}),
                                className="chat-message bot-message",
                                style={
                                    "padding": "12px 16px",
                                    "borderRadius": "15px",
                                    "backgroundColor": COLORS['chatbot']['bot_message'],
                                    "color": COLORS['chatbot']['bot_text'],
                                    "maxWidth": "80%",
                                    "marginBottom": "12px"
                                }
                            )
                        ],
                        style={
                            'height': 'calc(100% - 120px)',
                            'overflowY': 'auto',
                            'backgroundColor': COLORS['chatbot']['background'],
                            'borderRadius': '12px',
                            'padding': '16px',
                            'border': '1px solid #dee2e6'
                        }
                    ),
                    # User input and send button
                    html.Div(
                        [
                            dbc.InputGroup(
                                [
                                    dcc.Input(
                                        id="user-input",
                                        type="text",
                                        placeholder="Ask me anything about your data...",
                                        style={
                                            'borderRadius': '24px',
                                            'padding': '12px 20px',
                                            'flexGrow': 1
                                        },
                                        className="form-control"
                                    ),
                                    dbc.Button(
                                        html.I(className="fas fa-paper-plane"),
                                        id="send-button",
                                        color="primary",
                                        style={'borderRadius': '50%',
                                               'padding': '12px 16px'}
                                    ),
                                ],
                                className="mt-3",
                                style={'alignItems': 'center'}
                            )
                        ],
                        style={'marginTop': '16px'}
                    )
                ],
                className="d-flex flex-column justify-content-between",
                style={
                    'padding': '16px',
                    'height': '400px',
                    'borderRadius': '0 0 12px 12px'
                }
            ),
        ],
        className="shadow-sm h-100",
        style={
            'borderRadius': '12px',
            'border': 'none',
            'height': '100%'
        }
    )


def create_charts():
    """Create the enhanced charts section"""
    return dbc.Row(
        [
            # Sales Trend Chart
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.H5("Sales Trend", className="mb-0"),
                                style={
                                    'backgroundColor': '#f8f9fa',
                                    'borderBottom': '1px solid #dee2e6',
                                    'padding': '16px',
                                    'borderRadius': '12px 12px 0 0'
                                }
                            ),
                            dbc.CardBody(
                                dcc.Loading(
                                    id="loading-sales-trend",
                                    children=[
                                        dcc.Graph(
                                            id="sales-trend-chart",
                                            config={
                                                'displayModeBar': True,
                                                'scrollZoom': False,
                                                'displaylogo': False,
                                                'modeBarButtonsToRemove': [
                                                    'zoomIn2d', 'zoomOut2d', 'lasso2d', 'toggleSpikelines'
                                                ]
                                            },
                                            style={'height': '350px'}
                                        )
                                    ],
                                    type="circle",
                                    color="#00aaff"
                                ),
                                style={'padding': '16px'}
                            )
                        ],
                        className="shadow-sm mb-4",
                        style={'borderRadius': '12px', 'border': 'none'}
                    )
                ],
                width=6
            ),
            # Category Sales Chart
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.H5("Category Sales", className="mb-0"),
                                style={
                                    'backgroundColor': '#f8f9fa',
                                    'borderBottom': '1px solid #dee2e6',
                                    'padding': '16px',
                                    'borderRadius': '12px 12px 0 0'
                                }
                            ),
                            dbc.CardBody(
                                dcc.Loading(
                                    id="loading-category-sales",
                                    children=[
                                        dcc.Graph(
                                            id="category-sales-chart",
                                            config={
                                                'displayModeBar': True,
                                                'scrollZoom': False,
                                                'displaylogo': False,
                                                'modeBarButtonsToRemove': [
                                                    'zoomIn2d', 'zoomOut2d', 'lasso2d', 'toggleSpikelines'
                                                ]
                                            },
                                            style={'height': '350px'}
                                        )
                                    ],
                                    type="circle",
                                    color="#00aaff"
                                ),
                                style={'padding': '16px'}
                            )
                        ],
                        className="shadow-sm mb-4",
                        style={'borderRadius': '12px', 'border': 'none'}
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
        dbc.CardBody([
            html.H5("Custom Chart Controls", className="card-title mb-3"),
            dbc.Row([
                dbc.Col([
                    html.Label("X-Axis", className="form-label"),
                    dcc.Dropdown(
                        id='x-axis-dropdown',
                        options=[{'label': col, 'value': col}
                                 for col in df.columns],
                        value=NUMERIC_COLUMNS[0] if NUMERIC_COLUMNS else CATEGORICAL_COLUMNS[0],
                        placeholder="Select a column for X-Axis",
                        className="mb-3"
                    ),
                ], width=6),
                dbc.Col([
                    html.Label("Y-Axis", className="form-label"),
                    dcc.Dropdown(
                        id='y-axis-dropdown',
                        options=[{'label': col, 'value': col}
                                 for col in NUMERIC_COLUMNS],
                        value=NUMERIC_COLUMNS[1] if len(
                            NUMERIC_COLUMNS) > 1 else None,
                        placeholder="Select a column for Y-Axis",
                        className="mb-3"
                    ),
                ], width=6),
            ], className="mb-4"),
            html.Label("Chart Type", className="form-label"),
            dcc.Dropdown(
                id='chart-type-dropdown',
                options=[
                    {'label': 'Line Chart', 'value': 'line'},
                    {'label': 'Bar Chart', 'value': 'bar'},
                    {'label': 'Scatter Plot', 'value': 'scatter'},
                ],
                value='line',
                placeholder="Select chart type",
                className="mb-4"
            ),
            html.Label("Aggregation", className="form-label"),
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
                className="mb-4"
            ),
        ]),
        className="shadow-sm mb-4"
    )


# Main layout
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
        dbc.Col(create_custom_chart_controls(), width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    dcc.Loading(
                        id="loading-graph",
                        children=[
                            dcc.Graph(
                                id='custom-graph',
                                style={'height': '600px',
                                       'borderRadius': '10px'}
                            )
                        ],
                        type="circle",  # Choose between "circle" or "default"
                        color="#00aaff"  # Loading spinner color
                    )
                ]),
                className="shadow-sm"
            ),
            width=8
        )
    ])

], fluid=True, style={"backgroundColor": COLORS['background'], "padding": "24px"})
