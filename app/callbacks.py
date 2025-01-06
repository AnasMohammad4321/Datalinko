from dash import Input, Output
import pandas as pd
import plotly.graph_objects as go
from utils import COLORS

# Load and preprocess data
df = pd.read_csv("./data/raw/data.csv", low_memory=False)
df["created_at"] = pd.to_datetime(df["created_at"])

def register_callbacks(app):
    @app.callback(
        [
            Output("sales-trend-chart", "figure"),
            Output("category-sales-chart", "figure"),
            Output("payment-method-chart", "figure"),
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
        trend_data = filtered_df.groupby(pd.Grouper(key="created_at", freq='D'))["grand_total"].sum().reset_index()

        sales_trend_fig = go.Figure()
        sales_trend_fig.add_trace(go.Scatter(
            x=trend_data["created_at"],
            y=trend_data["grand_total"],
            mode='lines',
            fill='tonexty',
            line=dict(color=COLORS['secondary']),
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

        # Category sales chart
        category_data = filtered_df.groupby("product_category")["grand_total"].sum().sort_values(ascending=True).reset_index()

        category_sales_fig = go.Figure()
        category_sales_fig.add_trace(go.Bar(
            x=category_data["grand_total"],
            y=category_data["product_category"],
            orientation='h',
            marker_color=COLORS['secondary'],
        ))
        category_sales_fig.update_layout(
            title="Sales by Category",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=40, b=0),
            yaxis=dict(gridcolor='rgba(0,0,0,0.1)', zerolinecolor='rgba(0,0,0,0.1)'),
            xaxis=dict(gridcolor='rgba(0,0,0,0.1)', zerolinecolor='rgba(0,0,0,0.1)'),
        )

        # Payment method chart
        payment_data = filtered_df["payment_method"].value_counts().reset_index()
        payment_data.columns = ["payment_method", "count"]

        payment_method_fig = go.Figure(data=[go.Pie(
            labels=payment_data["payment_method"],
            values=payment_data["count"],
            hole=.4,
            marker_colors=COLORS['chart_colors'],
        )])
        payment_method_fig.update_layout(
            title="Payment Methods",
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            margin=dict(l=0, r=0, t=40, b=0),
        )

        # Metrics
        total_sales = f"${filtered_df['grand_total'].sum():,.2f}"
        total_orders = f"{filtered_df['item_id'].nunique():,}"
        avg_order_value = f"${filtered_df['grand_total'].mean():,.2f}" if not filtered_df.empty else "$0.00"

        return sales_trend_fig, category_sales_fig, payment_method_fig, total_sales, total_orders, avg_order_value
