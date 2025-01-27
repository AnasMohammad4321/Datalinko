import plotly.express as px
import pandas as pd


def load_data():
    df = pd.read_csv("./data/raw/sample_data.csv", low_memory=False)
    print("df.columns: ", df.columns)
    df["created_at"] = pd.to_datetime(df["created_at"])
    return df


COLORS = {
    'primary': '#2C3E50',
    'secondary': '#18BC9C',
    'background': '#F8F9FA',
    'text': '#2C3E50',
    'chatbot': {
        'background': '#F8F9FA',
        'user_message': '#18BC9C',
        'bot_message': '#EBF5FB',
        'user_text': '#FFFFFF',
        'bot_text': '#2C3E50',
    },
    'border': '#E9ECEF',
    'hover': '#F1F2F6',
    'chart_colors': ['#18BC9C', '#3498DB', '#E74C3C', '#F39C12', '#9B59B6']
}


CHART_TYPES = {
    'line': {'function': px.line, 'name': 'Line Chart'},
    'bar': {'function': px.bar, 'name': 'Bar Chart'},
    'scatter': {'function': px.scatter, 'name': 'Scatter Plot'},
}

AGGREGATIONS = {
    'sum': 'sum',
    'mean': 'mean',
    'count': 'count',
    'min': 'min',
    'max': 'max',
}

LIGHT_THEME = {
    "background": "#f8f9fa",
    "text": "#212529",
    "card": "#ffffff",
    "border": "1px solid rgba(0,0,0,0.1)",
    "button": "#0d6efd",
}

DARK_THEME = {
    "background": "#212529",
    "text": "#f8f9fa",
    "card": "#343a40",
    "border": "1px solid rgba(255,255,255,0.1)",
    "button": "#0d6efd",
}
