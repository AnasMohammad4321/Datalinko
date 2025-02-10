from dash import dcc, html
import dash_bootstrap_components as dbc
from datetime import datetime

CARD_BORDER_RADIUS = '12px'
PRIMARY_COLOR = '#0d6efd'
SHADOW_SM = '0 4px 8px rgba(0,0,0,0.1)'
TRANSITION = 'all 0.3s ease'

def format_timestamp():
    return datetime.now().strftime("%I:%M %p")

def create_message_style(is_bot=True):
    return {
        "padding": "10px 14px",
        "borderRadius": "18px",
        "backgroundColor": f"rgba(13, 110, 253, {0.15 if is_bot else 0.05})",
        "color": "#2c3e50",
        "maxWidth": "80%",
        "marginBottom": "10px",
        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",  # Lighter shadow for cleaner UI
        "marginLeft": "0" if is_bot else "auto",
        "border": f"1px solid {'rgba(13, 110, 253, 0.3)' if is_bot else 'rgba(108, 117, 125, 0.3)'}",
        "fontSize": "14px",
        "lineHeight": "1.6"
    }


def create_message_bubble(message, is_bot=True, timestamp=None):
    timestamp = timestamp or format_timestamp()
    return html.Div(
        dbc.Row(
            [
                dbc.Col(
                    html.I(
                        className=f"fas {'fa-robot' if is_bot else 'fa-user'}",
                        style={'color': PRIMARY_COLOR if is_bot else '#6c757d', 'fontSize': '1rem'}  # Font size adjusted
                    ),
                    width="auto"
                ),
                dbc.Col(
                    [
                        html.Div(
                            dcc.Markdown(message), 
                            style={'marginBottom': '4px'}
                        ),
                        html.Small(timestamp, className="text-muted", style={'fontSize': '0.65rem'})  # Font size adjusted
                    ],
                    style={'paddingLeft': '10px'}
                )
            ],
            align="start",
            justify="start" if is_bot else "end"
        ),
        className=f"chat-message {'bot-message' if is_bot else 'user-message'}",
        style=create_message_style(is_bot)
    )

def create_typing_indicator():
    return html.Div(
        dbc.Row(
            [
                dbc.Col(html.I(className="fas fa-robot", style={'color': PRIMARY_COLOR, 'fontSize': '1.2rem'}), width="auto"),
                dbc.Col(html.Div([html.Span("●", className="typing-dot"), html.Span("●", className="typing-dot"), html.Span("●", className="typing-dot")], style={'display': 'flex', 'gap': '4px', 'alignItems': 'center', 'padding': '8px'}), style={'paddingLeft': '10px'})
            ],
            align="center"
        ),
        id="typing-indicator",
        style={**create_message_style(True), 'display': 'none', 'maxWidth': '100px'}
    )


def create_chatbot():
    return dbc.Card(
        [
            # Header
            dbc.CardHeader(
                dbc.Row([
                    dbc.Col(
                        html.I(
                            className="fas fa-robot me-2",
                            style={'color': PRIMARY_COLOR}
                        ),
                        width='auto'
                    ),
                    dbc.Col(
                        html.H5("Analytics Assistant", className="mb-0")
                    ),
                    dbc.Col(
                        html.Button(
                            html.I(className="fas fa-trash-alt"),
                            id="clear-chat",
                            className="btn btn-link text-muted",
                            style={
                                'padding': '4px',
                                'float': 'right',
                                'fontSize': '0.9rem'
                            },
                            title="Clear conversation"
                        ),
                        width='auto'
                    )
                ], align="center"),
                style={
                    'backgroundColor': '#ffffff',
                    'borderBottom': '1px solid rgba(0,0,0,0.1)',
                    'padding': '20px',
                    'borderRadius': f'{CARD_BORDER_RADIUS} {CARD_BORDER_RADIUS} 0 0'
                }
            ),
            
            # Body
            dbc.CardBody(
                [
                    # Chat Display
                    html.Div(
                        [
                            create_message_bubble(
                                "Hello! I'm your analytics assistant. How can I help you analyze your data today?",
                                is_bot=True
                            ),
                            create_typing_indicator()
                        ],
                        id="chat-display",
                        style={
                            'height': 'calc(100% - 80px)',
                            'overflowY': 'auto',
                            'backgroundColor': '#ffffff',
                            'borderRadius': '12px',
                            'padding': '20px',
                            'scrollBehavior': 'smooth'
                        }
                    ),
                    
                    # Input Area
                    html.Div(
                        [
                            dbc.InputGroup(
                                [
                                    dcc.Input(
                                        id="user-input",
                                        type="text",
                                        placeholder="Ask about your data analysis...",
                                        # autocomplete="off",
                                        style={
                                            'borderRadius': '20px',
                                            'padding': '10px 20px',
                                            'border': '1.5px solid #ccc',
                                            'fontSize': '0.95rem',
                                            'flexGrow': 1,
                                            'outline': 'none'
                                        },
                                        className="form-control",
                                        n_submit=0
                                    ),
                                    dbc.Button(
                                        children=[
                                            html.I(
                                                className="fas fa-paper-plane",
                                                style={
                                                    'marginRight': '8px',
                                                    'fontSize': '0.9rem'
                                                }
                                            ),
                                            html.Span(
                                                "Send",
                                                style={
                                                    'fontWeight': '600',
                                                    'letterSpacing': '0.3px'
                                                }
                                            )
                                        ],
                                        id="send-button",
                                        color="primary",
                                        style={
                                            'borderRadius': '25px',
                                            'padding': '8px 24px',
                                            'height': '45px',
                                            'marginLeft': '10px',
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'justifyContent': 'center',
                                            'boxShadow': '0 2px 6px rgba(13, 110, 253, 0.15)',
                                            'transition': 'all 0.2s ease',
                                            'backgroundColor': PRIMARY_COLOR,
                                            'border': 'none',
                                            'minWidth': '100px',
                                            'cursor': 'pointer',
                                        },
                                        className="send-button-hover"
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
                    'borderRadius': f'0 0 {CARD_BORDER_RADIUS} {CARD_BORDER_RADIUS}'
                }
            ),
        ],
        className="shadow-sm h-100",
        style={
            'borderRadius': CARD_BORDER_RADIUS,
            'border': 'none',
            'backgroundColor': '#ffffff',
            'transition': TRANSITION,
            'height': '100%'
        }
    )

