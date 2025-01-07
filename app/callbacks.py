from dash import Input, Output, callback, no_update, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Load and preprocess data
df = pd.read_csv("./data/raw/sample_data.csv", low_memory=False)
df["created_at"] = pd.to_datetime(df["created_at"])

# Column classifications
NUMERIC_COLUMNS = df.select_dtypes(include=['number']).columns.tolist()
CATEGORICAL_COLUMNS = df.select_dtypes(
    include=['object', 'category']).columns.tolist()

# Chart type configurations
CHART_TYPES = {
    'line': {'function': px.line, 'name': 'Line Chart'},
    'bar': {'function': px.bar, 'name': 'Bar Chart'},
    'scatter': {'function': px.scatter, 'name': 'Scatter Plot'},
}

# Aggregation functions
AGGREGATIONS = {
    'sum': 'sum',
    'mean': 'mean',
    'count': 'count',
    'min': 'min',
    'max': 'max',
}


def register_callbacks(app):
    @app.callback(
        [
            Output("sales-trend-chart", "figure"),
            Output("category-sales-chart", "figure"),
            Output("total-sales", "children"),
            Output("total-orders", "children"),
            Output("avg-order-value", "children"),
        ],
        [
            Input("date-range", "start_date"),
            Input("date-range", "end_date"),
            Input("order-status", "value"),
        ]
    )
    def update_dashboard(start_date, end_date, order_status):
        # Filter data
        filtered_df = df[
            (df["created_at"] >= start_date) &
            (df["created_at"] <= end_date) &
            (df["order_status"].isin(order_status))
        ]

        # Sales trend chart
        trend_data = filtered_df.groupby(
            pd.Grouper(key="created_at", freq='D'))["grand_total"].sum().reset_index()
        sales_trend_fig = go.Figure()
        sales_trend_fig.add_trace(go.Scatter(
            x=trend_data["created_at"],
            y=trend_data["grand_total"],
            mode='lines',
            fill='tonexty',
            line=dict(color='#18BC9C'),
            name='Sales'
        ))
        sales_trend_fig.update_layout(
            title="Daily Sales Trend",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            hovermode='x unified',
            margin=dict(l=0, r=0, t=40, b=0),
            yaxis=dict(gridcolor='rgba(0,0,0,0.1)',
                       zerolinecolor='rgba(0,0,0,0.1)'),
            xaxis=dict(gridcolor='rgba(0,0,0,0.1)',
                       zerolinecolor='rgba(0,0,0,0.1)'),
        )

        # Category sales chart
        category_data = filtered_df.groupby("product_category")[
            "grand_total"].sum().sort_values(ascending=True).reset_index()
        category_sales_fig = go.Figure()
        category_sales_fig.add_trace(go.Bar(
            x=category_data["grand_total"],
            y=category_data["product_category"],
            orientation='h',
            marker_color='#18BC9C',
        ))
        category_sales_fig.update_layout(
            title="Sales by Category",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=40, b=0),
            yaxis=dict(gridcolor='rgba(0,0,0,0.1)',
                       zerolinecolor='rgba(0,0,0,0.1)'),
            xaxis=dict(gridcolor='rgba(0,0,0,0.1)',
                       zerolinecolor='rgba(0,0,0,0.1)'),
        )

        # Calculate metrics
        total_sales = f"${filtered_df['grand_total'].sum():,.2f}"
        total_orders = f"{filtered_df['item_id'].nunique():,}"
        avg_order_value = f"${filtered_df['grand_total'].mean():,.2f}" if not filtered_df.empty else "$0.00"

        return sales_trend_fig, category_sales_fig, total_sales, total_orders, avg_order_value

    @app.callback(
        Output('y-axis-dropdown', 'options'),
        Input('x-axis-dropdown', 'value')
    )
    def update_yaxis_options(selected_x):
        """Update Y-axis options based on the selected X-axis"""
        if selected_x in NUMERIC_COLUMNS:
            return [{'label': col, 'value': col} for col in NUMERIC_COLUMNS]
        return [{'label': col, 'value': col}
                for col in NUMERIC_COLUMNS if col != selected_x]

    @app.callback(
        Output('custom-graph', 'figure'),
        [
            Input('x-axis-dropdown', 'value'),
            Input('y-axis-dropdown', 'value'),
            Input('chart-type-dropdown', 'value'),
            Input('aggregation-dropdown', 'value'),
        ]
    )
    def update_graph(x_axis, y_axis, chart_type, aggregation):
        """Update the custom graph based on user selections"""
        # Handle missing values
        if not x_axis or not y_axis:
            return go.Figure().update_layout(
                title="Please select valid X and Y axes",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )

        try:
            # Apply aggregation if specified
            if aggregation and aggregation in AGGREGATIONS:
                agg_func = AGGREGATIONS[aggregation]
                aggregated_df = df.groupby(x_axis).agg(
                    {y_axis: agg_func}).reset_index()
                x = aggregated_df[x_axis]
                y = aggregated_df[y_axis]
            else:
                x = df[x_axis]
                y = df[y_axis]

            # Generate figure using the appropriate chart type
            fig = CHART_TYPES[chart_type]['function'](
                x=x,
                y=y,
                labels={x_axis: x_axis, y_axis: y_axis},
                title=f"{y_axis} vs {x_axis} ({aggregation})" if aggregation else f"{y_axis} vs {x_axis}"
            )

            # Update layout for consistency
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=40, b=0),
                yaxis=dict(gridcolor='rgba(0,0,0,0.1)',
                           zerolinecolor='rgba(0,0,0,0.1)'),
                xaxis=dict(gridcolor='rgba(0,0,0,0.1)',
                           zerolinecolor='rgba(0,0,0,0.1)'),
            )

            return fig

        except Exception as e:
            return go.Figure().update_layout(
                title=f"Error generating graph: {str(e)}",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )

    @app.callback(
        Output("chat-display", "children"),
        [
            Input("send-button", "n_clicks"),
            Input("user-input", "value")
        ]
    )
    def update_chat(n_clicks, user_input):
        """Update chat display with user messages"""
        if not n_clicks or not user_input:
            return no_update

        return [
            html.Div(
                user_input,
                className="chat-message user-message",
                style={
                    "backgroundColor": "#18BC9C",
                    "color": "white",
                    "padding": "12px",
                    "borderRadius": "15px",
                    "marginBottom": "8px",
                    "maxWidth": "80%",
                    "marginLeft": "auto"
                }
            )
        ]
