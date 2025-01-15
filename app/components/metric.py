from utils import generate_metric_card
import dash_bootstrap_components as dbc


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
