from dash import dcc, html
import dash_bootstrap_components as dbc


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
