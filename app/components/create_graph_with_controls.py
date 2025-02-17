from components.custom_chart_control import create_custom_chart_controls
from dash import dcc, html
import dash_bootstrap_components as dbc

def create_graph_with_controls(id_suffix=""):
    return html.Div([
        dbc.Row([
            dbc.Col(create_custom_chart_controls(id_suffix), width=4, className="h-100"),
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
                                        id={'type': 'expand-button', 'index': id_suffix},
                                        style={'boxShadow': 'none'}
                                    ),
                                    dbc.Button(
                                        html.I(className="fas fa-download"),
                                        color="link",
                                        size="sm",
                                        className="text-muted",
                                        id={'type': 'download-button', 'index': id_suffix},
                                        style={'boxShadow': 'none'}
                                    ),
                                    dbc.Button(
                                        html.I(className="fas fa-trash"),
                                        color="link",
                                        size="sm",
                                        className="text-muted",
                                        id={'type': 'delete-button', 'index': id_suffix},
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
                            id={'type': 'loading-graph', 'index': id_suffix},
                            children=[
                                dcc.Graph(
                                    id={'type': 'custom-graph', 'index': id_suffix},
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
        ], className="align-items-stretch mb-5")
    ], id={'type': 'graph-container', 'index': id_suffix})