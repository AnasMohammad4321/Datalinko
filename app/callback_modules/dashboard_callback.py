import requests
from dash import Input, Output, callback, dcc, html
import plotly.graph_objects as go
import pandas as pd

API_URL = "http://0.0.0.0:8000/get_filtered_data"  

def fetch_filtered_data(start_date, end_date, order_status):
    """Fetch filtered data from the API."""
    if not start_date or not end_date or not order_status:
        return pd.DataFrame()  

    order_status_str = ",".join(order_status)  
    params = {"start_date": start_date, "end_date": end_date, "order_status": order_status_str}

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if "data" in data:
            df = pd.DataFrame(data["data"])
        else:
            return pd.DataFrame()

        if "created_at" in df:
            df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

        if "grand_total" in df:
            df["grand_total"] = pd.to_numeric(df["grand_total"], errors="coerce").fillna(0)

        return df

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

def generate_sales_trend_chart(trend_data):
    """Create the sales trend figure."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trend_data["created_at"],
        y=trend_data["grand_total"],
        mode="lines",
        fill="tonexty",
        line=dict(color="#18BC9C"),
        name="Sales"
    ))
    fig.update_layout(
        title="Daily Sales Trend",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified",
        margin=dict(l=0, r=0, t=40, b=0),
        yaxis=dict(gridcolor="rgba(0,0,0,0.1)", zerolinecolor="rgba(0,0,0,0.1)"),
        xaxis=dict(gridcolor="rgba(0,0,0,0.1)", zerolinecolor="rgba(0,0,0,0.1)"),
    )
    return fig

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
        ],
    )
    def update_dashboard(start_date, end_date, order_status):
        print(f"Fetching data for {start_date} to {end_date} | Statuses: {order_status}")
        filtered_df = fetch_filtered_data(start_date, end_date, order_status)

        if filtered_df.empty:
            return go.Figure(), go.Figure(), "$0.00", "0", "$0.00"

        required_cols = ["created_at", "grand_total", "product_category", "item_id"]
        missing_cols = [col for col in required_cols if col not in filtered_df.columns]
        if missing_cols:
            print(f"Missing columns: {missing_cols}")
            return go.Figure(), go.Figure(), "$0.00", "0", "$0.00"

        trend_data = (
            filtered_df.groupby(pd.Grouper(key="created_at", freq="D"))["grand_total"]
            .sum()
            .reset_index()
        )
        category_data = (
            filtered_df.groupby("product_category")["grand_total"]
            .sum()
            .reset_index()
            .sort_values(by="grand_total", ascending=False)
        )

        total_sales = f"${filtered_df['grand_total'].sum():,.2f}"
        total_orders = f"{filtered_df['item_id'].nunique():,}"
        avg_order_value = f"${filtered_df['grand_total'].mean():,.2f}" if not filtered_df.empty else "$0.00"

        sales_trend_fig = generate_sales_trend_chart(trend_data)

        category_sales_fig = go.Figure()
        category_sales_fig.add_trace(
            go.Bar(
                x=category_data["grand_total"],
                y=category_data["product_category"],
                orientation="h",
                marker_color="#18BC9C",
            )
        )
        category_sales_fig.update_layout(
            title="Sales by Category",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=40, b=0),
            yaxis=dict(gridcolor="rgba(0,0,0,0.1)", zerolinecolor="rgba(0,0,0,0.1)"),
            xaxis=dict(gridcolor="rgba(0,0,0,0.1)", zerolinecolor="rgba(0,0,0,0.1)"),
        )

        return sales_trend_fig, category_sales_fig, total_sales, total_orders, avg_order_value

