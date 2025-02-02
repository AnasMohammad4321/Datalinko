from dash import Input, Output, callback, no_update, html, State, ALL, MATCH, ctx
import pandas as pd
import plotly.graph_objects as go
from constants.generic_constants import CHART_TYPES, AGGREGATIONS, LIGHT_THEME, DARK_THEME, load_data
from components.create_graph_with_controls import create_graph_with_controls

df = load_data()

NUMERIC_COLUMNS = df.select_dtypes(include=['number']).columns.tolist()
CATEGORICAL_COLUMNS = df.select_dtypes(include=['object', 'category']).columns.tolist()

def register_dashboard_callback(app):
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
        filtered_df = df[
            (df["created_at"] >= start_date) &
            (df["created_at"] <= end_date) &
            (df["order_status"].isin(order_status))
        ]
        trend_data = filtered_df.groupby(
            pd.Grouper(key="created_at", freq='D'))["grand_total"].sum().reset_index()
        
        # Create sales trend figure
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
            yaxis=dict(gridcolor='rgba(0,0,0,0.1)', zerolinecolor='rgba(0,0,0,0.1)'),
            xaxis=dict(gridcolor='rgba(0,0,0,0.1)', zerolinecolor='rgba(0,0,0,0.1)'),
        )

        # Create category sales figure
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
            yaxis=dict(gridcolor='rgba(0,0,0,0.1)', zerolinecolor='rgba(0,0,0,0.1)'),
            xaxis=dict(gridcolor='rgba(0,0,0,0.1)', zerolinecolor='rgba(0,0,0,0.1)'),
        )

        # Calculate metrics
        total_sales = f"${filtered_df['grand_total'].sum():,.2f}"
        total_orders = f"{filtered_df['item_id'].nunique():,}"
        avg_order_value = f"${filtered_df['grand_total'].mean():,.2f}" if not filtered_df.empty else "$0.00"

        return sales_trend_fig, category_sales_fig, total_sales, total_orders, avg_order_value