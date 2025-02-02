from dash import Input, Output, callback, no_update, html, State, ALL, MATCH, ctx
import pandas as pd
import plotly.graph_objects as go
from constants.generic_constants import CHART_TYPES, AGGREGATIONS, LIGHT_THEME, DARK_THEME, load_data
from components.create_graph_with_controls import create_graph_with_controls

df = load_data()

NUMERIC_COLUMNS = df.select_dtypes(include=['number']).columns.tolist()
CATEGORICAL_COLUMNS = df.select_dtypes(include=['object', 'category']).columns.tolist()

def register_graph_update_callback(app):
    @app.callback(
        Output({'type': 'custom-graph', 'index': MATCH}, 'figure'),
        [
            Input({'type': 'x-axis-dropdown', 'index': MATCH}, 'value'),
            Input({'type': 'y-axis-dropdown', 'index': MATCH}, 'value'),
            Input({'type': 'chart-type-dropdown', 'index': MATCH}, 'value'),
            Input({'type': 'aggregation-dropdown', 'index': MATCH}, 'value'),
        ]
    )
    def update_graph(x_axis, y_axis, chart_type, aggregation):
        if not x_axis or not y_axis:
            return go.Figure().update_layout(
                title="Please select valid X and Y axes",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )

        try:
            if aggregation and aggregation in AGGREGATIONS:
                agg_func = AGGREGATIONS[aggregation]
                aggregated_df = df.groupby(x_axis).agg(
                    {y_axis: agg_func}).reset_index()
                x = aggregated_df[x_axis]
                y = aggregated_df[y_axis]
            else:
                x = df[x_axis]
                y = df[y_axis]

            fig = CHART_TYPES[chart_type]['function'](
                x=x,
                y=y,
                labels={x_axis: x_axis, y_axis: y_axis},
                title=f"{y_axis} vs {x_axis} ({aggregation})" if aggregation else f"{y_axis} vs {x_axis}"
            )

            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=40, b=0),
                yaxis=dict(gridcolor='rgba(0,0,0,0.1)', zerolinecolor='rgba(0,0,0,0.1)'),
                xaxis=dict(gridcolor='rgba(0,0,0,0.1)', zerolinecolor='rgba(0,0,0,0.1)'),
            )

            return fig

        except Exception as e:
            return go.Figure().update_layout(
                title=f"Error generating graph: {str(e)}",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )