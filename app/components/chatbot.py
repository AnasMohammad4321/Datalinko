from dash import dcc, html
import dash_bootstrap_components as dbc

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