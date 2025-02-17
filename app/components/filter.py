from dash import dcc, html
import dash_bootstrap_components as dbc
from app.constants.generic_constants import load_data
import requests


API_URL = "http://0.0.0.0:8000/get_filters"

def fetch_filter_data():
    """Fetch order statuses and date range from API."""
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching filter data: {e}")
        return {}


filter_data = fetch_filter_data()

def create_filters():
    """Create the filters section with improved UI/UX."""
    if not filter_data:
        return dbc.Alert("No filter data available. Please check API.", color="danger")

    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Date Range", className="fw-bold mb-2"),
                    dcc.DatePickerRange(
                        id="date-range",
                        start_date=filter_data.get("start_date"),
                        end_date=filter_data.get("end_date"),
                        style={"width": "100%", "padding": "0.5rem", "borderRadius": "8px"}
                    )
                ], xs=12, md=6),
                dbc.Col([
                    html.Label("Order Status", className="fw-bold mb-2"),
                    dcc.Dropdown(
                        id="order-status",
                        options=[
                            {"label": status.title(), "value": status}
                            for status in filter_data.get("order_statuses", [])
                        ],
                        value=filter_data.get("order_statuses", []),
                        multi=True,
                        style={"width": "100%", "padding": "0.5rem", "borderRadius": "8px"}
                    )
                ], xs=12, md=6)
            ])
        ])
    ], className="mb-4 shadow-sm filter-card",
        style={'borderRadius': '12px', 'border': 'none', 'backgroundColor': 'white'}
    )