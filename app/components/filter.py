from dash import dcc, html
import dash_bootstrap_components as dbc
from app.constants.generic_constants import load_data

df = load_data()


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
