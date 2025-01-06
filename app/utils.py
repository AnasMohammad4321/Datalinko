import dash_bootstrap_components as dbc
from dash import html
import openai

# Custom color palette
COLORS = {
    'primary': '#2C3E50',
    'secondary': '#18BC9C',
    'background': '#F8F9FA',
    'text': '#2C3E50',
    'chart_colors': ['#18BC9C', '#3498DB', '#E74C3C', '#F39C12', '#9B59B6']
}


def generate_metric_card(id, label, icon):
    return dbc.Card(
        dbc.CardBody([
            html.Div([  # This is now correct
                html.I(className=f"fas {icon} fa-2x me-2",
                       style={'color': COLORS['secondary']}),
                html.H5(label, className="card-title mb-0")
            ], className="d-flex align-items-center mb-3"),
            html.Div(id=id, className="card-text",
                     style={"fontSize": "24px", "fontWeight": "bold", "color": COLORS['primary']}),
        ]),
        className="shadow-sm h-100",
        style={"backgroundColor": "white"}
    )


def generate_report(data_summary):
    prompt = f"Generate a detailed business performance report using the following data summary: {data_summary}"

    response = openai.Completion.create(
        model="text-davinci-003",  # You can choose another model like GPT-4 if preferred
        prompt=prompt,
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].text.strip()
