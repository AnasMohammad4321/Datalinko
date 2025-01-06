from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
from utils import generate_metric_card

# Load and preprocess data
df = pd.read_csv("./data/raw/data.csv", low_memory=False)
df["created_at"] = pd.to_datetime(df["created_at"])

# Enhanced color palette
COLORS = {
    'primary': '#2C3E50',
    'secondary': '#18BC9C',
    'background': '#F8F9FA',
    'text': '#2C3E50',
    'chatbot_background': '#F8F9FA',
    'user_message': '#18BC9C',
    'bot_message': '#EBF5FB',
    'bot_text': '#2C3E50',
    'user_text': '#FFFFFF',
    'border': '#E9ECEF',
    'hover': '#F1F2F6',
    'chart_colors': ['#18BC9C', '#3498DB', '#E74C3C', '#F39C12', '#9B59B6']
}

# Layout of the app
layout = dbc.Container([

    # Enhanced Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("E-Commerce Analytics Dashboard",
                        className="display-4 mb-2",
                        style={
                            'color': COLORS['primary'],
                            'fontWeight': '600',
                            'letterSpacing': '-0.5px'
                        }),
                html.P("Monitor your business performance in real-time",
                       className="lead",
                       style={
                           'color': '#6C757D',
                           'fontSize': '1.1rem'
                       })
            ], style={'padding': '20px 0'})
        ], width=12)
    ], className="mb-4"),

    # Enhanced Action Bar
    dbc.Row([
        dbc.Col([
            dbc.Button([
                html.I(className="fas fa-file-export me-2"),
                "Generate Report"
            ], id="generate-report-button",
                color="primary",
                size="lg",
                className="shadow-sm",
                style={
                    'borderRadius': '8px',
                    'padding': '12px 24px',
                    'fontWeight': '500'
            }),
        ], width=6),

        dbc.Col([
            dcc.Upload(
                id="upload-data",
                children=dbc.Button([
                    html.I(className="fas fa-upload me-2"),
                    "Upload Data"
                ],
                    color="secondary",
                    size="lg",
                    className="shadow-sm",
                    style={
                        'borderRadius': '8px',
                        'padding': '12px 24px',
                        'fontWeight': '500'
                }),
                style={
                    'width': '100%',
                    'textAlign': 'center'
                }
            )
        ], width=6)
    ], className="mb-4"),

    # Enhanced Filters Section at the top
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Date Range",
                                       className="fw-bold mb-2",
                                       style={
                                           'color': COLORS['primary'],
                                           'fontSize': '0.9rem'
                                       }),
                            dcc.DatePickerRange(
                                id="date-range",
                                start_date=df["created_at"].min(),
                                end_date=df["created_at"].max(),
                                className="mb-2",
                                style={
                                    "zIndex": 1000,
                                    "width": "100%"
                                }
                            ),
                        ], xs=12, md=6),

                        dbc.Col([
                            html.Label("Order Status",
                                       className="fw-bold mb-2",
                                       style={
                                           'color': COLORS['primary'],
                                           'fontSize': '0.9rem'
                                       }),
                            dcc.Dropdown(
                                id="order-status",
                                options=[{"label": status.title(), "value": status}
                                         for status in df["order_status"].unique()],
                                value=df["order_status"].unique(),
                                multi=True,
                                className="mb-2",
                                style={
                                    'borderRadius': '8px'
                                }
                            ),
                        ], xs=12, md=6),
                    ])
                ])
            ], className="mb-4 shadow-sm", style={'borderRadius': '12px', 'border': 'none'})
        ], width=12)
    ], className="mb-4"),

    # Enhanced Metrics Row
    dbc.Row([
        dbc.Col(generate_metric_card("total-sales", "Total Sales",
                "fa-dollar-sign"), xs=12, md=4, className="mb-3"),
        dbc.Col(generate_metric_card("total-orders", "Total Orders",
                "fa-shopping-cart"), xs=12, md=4, className="mb-3"),
        dbc.Col(generate_metric_card("avg-order-value", "Avg Order Value",
                "fa-chart-line"), xs=12, md=4, className="mb-3"),
    ], className="mb-4 g-3"),

    # Enhanced Chatbot and Charts Section (3 Equal Columns)
    dbc.Row([
        dbc.Col([
            # Enhanced Chatbot Section
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Analytics Assistant",
                            className="mb-0",
                            style={
                                'color': COLORS['primary'],
                                'fontWeight': '600'
                            }),
                ], style={'backgroundColor': 'white', 'borderBottom': f'1px solid {COLORS["border"]}'}),
                dbc.CardBody([
                    # Chat Display
                    html.Div(id="chat-display",
                             children=[
                                html.Div([
                                    html.Div([
                                        html.I(className="fas fa-robot me-2"),
                                        "Hello! How can I assist you today?"
                                    ], style={
                                        'display': 'flex',
                                        'alignItems': 'center'
                                    })
                                ], className="chat-message bot-message",
                                    style={
                                    "padding": "12px 16px",
                                    "borderRadius": "15px",
                                    "backgroundColor": COLORS['bot_message'],
                                    "color": COLORS['bot_text'],
                                    "maxWidth": "80%",
                                    "marginBottom": "12px"
                                }),
                             ],
                             className="chat-display",
                             style={
                                 'height': 'calc(100% - 80px)',
                                 'overflowY': 'auto',
                                 'backgroundColor': COLORS['chatbot_background'],
                                 'borderRadius': '12px',
                                 'padding': '16px'
                             }),

                    # Enhanced Input Area
                    html.Div([
                        dcc.Input(
                            id="user-input",
                            type="text",
                            placeholder="Ask me anything about your data...",
                            className="form-control",
                            debounce=True,
                            style={
                                'width': '100%',
                                'borderRadius': '24px',
                                'padding': '12px 20px',
                                'border': f'1px solid {COLORS["border"]}',
                                'marginBottom': '8px'
                            }
                        ),
                        dbc.Button([
                            html.I(className="fas fa-paper-plane me-2"),
                            "Send"
                        ],
                            id="send-button",
                            color="primary",
                            className="w-100",
                            style={
                                'borderRadius': '24px',
                                'padding': '10px'
                        }),
                    ], className="input-area", style={'marginTop': '16px'})
                ], style={'height': '100%', 'padding': '16px'})
            ], className="shadow-sm", style={
                'height': '100%',
                'borderRadius': '12px',
                'border': 'none'
            })
        ], width=4, className="mb-4"),

        dbc.Col([
            # Sales Trend Chart
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Sales Trend",
                            className="mb-0",
                            style={
                                'color': COLORS['primary'],
                                'fontWeight': '600'
                            })
                ], style={'backgroundColor': 'white', 'borderBottom': f'1px solid {COLORS["border"]}'}),
                dbc.CardBody([
                    dcc.Graph(id="sales-trend-chart",
                             config={'displayModeBar': False})
                ], style={'padding': '16px'})
            ], className="shadow-sm mb-4",
                style={'borderRadius': '12px', 'border': 'none'}),
        ], width=4, className="mb-4"),

        dbc.Col([
            # Category Sales Chart
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Category Sales",
                            className="mb-0",
                            style={
                                'color': COLORS['primary'],
                                'fontWeight': '600'
                            })
                ], style={'backgroundColor': 'white', 'borderBottom': f'1px solid {COLORS["border"]}'}),
                dbc.CardBody([
                    dcc.Graph(id="category-sales-chart",
                             config={'displayModeBar': False})
                ], style={'padding': '16px'})
            ], className="shadow-sm h-100",
                style={'borderRadius': '12px', 'border': 'none'})
        ], width=4, className="mb-4"),
    ], className="g-4"),

    # Full-width Line Chart at the bottom
    dbc.Row([
        dbc.Col([
            # Payment Methods Chart
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Payment Methods",
                            className="mb-0",
                            style={
                                'color': COLORS['primary'],
                                'fontWeight': '600'
                            })
                ], style={'backgroundColor': 'white', 'borderBottom': f'1px solid {COLORS["border"]}'}),
                dbc.CardBody([
                    dcc.Graph(id="payment-method-chart",
                             config={'displayModeBar': False})
                ], style={'padding': '16px'})
            ], className="shadow-sm h-100",
                style={'borderRadius': '12px', 'border': 'none'})
        ], width=12),
    ], className="g-4"),
], fluid=True, style={
    "backgroundColor": COLORS['background'],
    "minHeight": "100vh",
    "padding": "24px"
})
