import dash_bootstrap_components as dbc
from dash import html
import openai
import pandas as pd
from constants.generic_constants import COLORS


def generate_metric_card(id, label, icon):
    return dbc.Card(
        dbc.CardBody([
            html.Div([
                html.I(className=f"fas {icon} fa-2x me-2",
                       style={'color': COLORS['secondary']}),
                html.H5(label, className="card-title mb-0")
            ], className="d-flex align-items-center mb-3"),
            html.Div(id=id, className="card-text",
                     style={"fontSize": "24px", "fontWeight": "bold", "color": COLORS['primary']}),
        ]),
        className="shadow-sm h-100 metric-card",
        style={"backgroundColor": "white", "transition": "all 0.3s ease-in-out",
               "borderRadius": "10px", "cursor": "pointer"}
    )


def generate_report(data_summary):
    prompt = f"Generate a detailed business performance report using the following data summary: {data_summary}"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].text.strip()
