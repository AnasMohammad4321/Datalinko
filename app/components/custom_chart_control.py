from dash import dcc, html
import dash_bootstrap_components as dbc
from constants.generic_constants import load_data

df = load_data()

NUMERIC_COLUMNS = df.select_dtypes(include=['number']).columns.tolist()
CATEGORICAL_COLUMNS = df.select_dtypes(
    include=['object', 'category']).columns.tolist()


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
