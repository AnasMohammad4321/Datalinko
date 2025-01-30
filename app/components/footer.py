from dash import html
import dash_bootstrap_components as dbc
from datetime import datetime
from constants.generic_constants import COLORS

def create_footer():
    """Create footer section with copyright and links"""
    return html.Footer(
        dbc.Container(
            dbc.Row([
                dbc.Col(
                    html.P(f"\u00A9 {datetime.now().year} DataLinko", 
                           className="text-muted mb-0"),
                    width=6
                ),
                dbc.Col(
                    html.Div([
                        html.A("Terms", href="#", className="text-muted text-decoration-none me-3"),
                        html.A("Privacy", href="#", className="text-muted text-decoration-none me-3"),
                        html.A("Contact", href="#", className="text-muted text-decoration-none")
                    ], className="text-end"),
                    width=6
                )
            ], className="align-items-center")
        ),
        className="mt-4 py-3",
        style={
            "backgroundColor": COLORS['background'],
            "borderTop": f"1px solid {COLORS['border']}",
            "borderRadius": "0 0 16px 16px",
        }
    )