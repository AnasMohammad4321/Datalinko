# import dash
# from dash import dcc, html, Input, Output
# import dash_bootstrap_components as dbc
# import plotly.express as px
# import plotly.graph_objects as go
# import pandas as pd
# from datetime import datetime, timedelta

# # Load and preprocess data
# df = pd.read_csv("./sample_data.csv")
# df["created_at"] = pd.to_datetime(df["created_at"])

# # Initialize Dash app with a modern Bootstrap theme
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# # Custom color palette
# COLORS = {
#     'primary': '#2C3E50',
#     'secondary': '#18BC9C',
#     'background': '#F8F9FA',
#     'text': '#2C3E50',
#     'chart_colors': ['#18BC9C', '#3498DB', '#E74C3C', '#F39C12', '#9B59B6']
# }


# def generate_metric_card(id, label, icon):
#     return dbc.Card(
#         dbc.CardBody([
#             html.Div([
#                 html.I(className=f"fas {icon} fa-2x me-2",
#                        style={'color': COLORS['secondary']}),
#                 html.H5(label, className="card-title mb-0")
#             ], className="d-flex align-items-center mb-3"),
#             html.Div(id=id, className="card-text",
#                      style={
#                          "fontSize": "24px",
#                          "fontWeight": "bold",
#                          "color": COLORS['primary']
#                      }),
#         ]),
#         className="shadow-sm h-100",
#         style={"backgroundColor": "white"}
#     )


# # Layout
# app.layout = dbc.Container([
#     # Header
#     dbc.Row([
#         dbc.Col([
#             html.H1("E-Commerce Analytics Dashboard",
#                     className="display-4 mb-2",
#                     style={'color': COLORS['primary']}),
#             html.P("Monitor your business performance in real-time",
#                    className="lead text-muted")
#         ], width=12)
#     ], className="mb-4 pt-4"),

#     # Filters Section
#     dbc.Card([
#         dbc.CardBody([
#             dbc.Row([
#                 dbc.Col([
#                     html.Label("Date Range",
#                                className="fw-bold mb-2",
#                                style={'color': COLORS['primary']}),
#                     dcc.DatePickerRange(
#                         id="date-range",
#                         start_date=df["created_at"].min(),
#                         end_date=df["created_at"].max(),
#                         className="mb-2",
#                         style={"zIndex": 1000}
#                     ),
#                 ], xs=12, md=6),

#                 dbc.Col([
#                     html.Label("Order Status",
#                                className="fw-bold mb-2",
#                                style={'color': COLORS['primary']}),
#                     dcc.Dropdown(
#                         id="order-status",
#                         options=[{"label": status.title(), "value": status}
#                                  for status in df["order_status"].unique()],
#                         value=df["order_status"].unique(),
#                         multi=True,
#                         className="mb-2"
#                     ),
#                 ], xs=12, md=6),
#             ])
#         ])
#     ], className="mb-4 shadow-sm"),

#     # Metrics Row
#     dbc.Row([
#         dbc.Col(generate_metric_card(
#             "total-sales", "Total Sales", "fa-dollar-sign"), xs=12, md=4),
#         dbc.Col(generate_metric_card(
#             "total-orders", "Total Orders", "fa-shopping-cart"), xs=12, md=4),
#         dbc.Col(generate_metric_card(
#             "avg-order-value", "Avg Order Value", "fa-chart-line"), xs=12, md=4),
#     ], className="mb-4 g-3"),

#     # Charts
#     dbc.Row([
#         dbc.Col([
#             dbc.Card([
#                 dbc.CardBody([
#                     dcc.Graph(id="sales-trend-chart",
#                              config={'displayModeBar': False})
#                 ])
#             ], className="shadow-sm")
#         ], width=12, className="mb-4"),
#     ]),

#     dbc.Row([
#         dbc.Col([
#             dbc.Card([
#                 dbc.CardBody([
#                     dcc.Graph(id="category-sales-chart",
#                              config={'displayModeBar': False})
#                 ])
#             ], className="shadow-sm h-100")
#         ], xs=12, md=6),
#         dbc.Col([
#             dbc.Card([
#                 dbc.CardBody([
#                     dcc.Graph(id="payment-method-chart",
#                              config={'displayModeBar': False})
#                 ])
#             ], className="shadow-sm h-100")
#         ], xs=12, md=6),
#     ], className="g-3"),

# ], fluid=True, style={"backgroundColor": COLORS['background'], "minHeight": "100vh", "padding": "20px"})


# @app.callback(
#     [
#         Output("sales-trend-chart", "figure"),
#         Output("category-sales-chart", "figure"),
#         Output("payment-method-chart", "figure"),
#         Output("total-sales", "children"),
#         Output("total-orders", "children"),
#         Output("avg-order-value", "children"),
#     ],
#     [
#         Input("date-range", "start_date"),
#         Input("date-range", "end_date"),
#         Input("order-status", "value"),
#     ]
# )
# def update_dashboard(start_date, end_date, order_status):
#     # Filter data
#     filtered_df = df[
#         (df["created_at"] >= start_date) &
#         (df["created_at"] <= end_date) &
#         (df["order_status"].isin(order_status))
#     ]

#     # Sales trend chart
#     trend_data = filtered_df.groupby(
#         pd.Grouper(key="created_at", freq='D'))["grand_total"].sum().reset_index()

#     sales_trend_fig = go.Figure()
#     sales_trend_fig.add_trace(go.Scatter(
#         x=trend_data["created_at"],
#         y=trend_data["grand_total"],
#         mode='lines',
#         fill='tonexty',
#         line=dict(color=COLORS['secondary']),
#         name='Sales'
#     ))
#     sales_trend_fig.update_layout(
#         title="Daily Sales Trend",
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         hovermode='x unified',
#         margin=dict(l=0, r=0, t=40, b=0),
#         yaxis=dict(
#             gridcolor='rgba(0,0,0,0.1)',
#             zerolinecolor='rgba(0,0,0,0.1)',
#         ),
#         xaxis=dict(
#             gridcolor='rgba(0,0,0,0.1)',
#             zerolinecolor='rgba(0,0,0,0.1)',
#         )
#     )

#     # Category sales chart
#     category_data = filtered_df.groupby("product_category")[
#         "grand_total"].sum().sort_values(ascending=True).reset_index()

#     category_sales_fig = go.Figure()
#     category_sales_fig.add_trace(go.Bar(
#         x=category_data["grand_total"],
#         y=category_data["product_category"],
#         orientation='h',
#         marker_color=COLORS['secondary'],
#     ))
#     category_sales_fig.update_layout(
#         title="Sales by Category",
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         margin=dict(l=0, r=0, t=40, b=0),
#         yaxis=dict(
#             gridcolor='rgba(0,0,0,0.1)',
#             zerolinecolor='rgba(0,0,0,0.1)',
#         ),
#         xaxis=dict(
#             gridcolor='rgba(0,0,0,0.1)',
#             zerolinecolor='rgba(0,0,0,0.1)',
#         )
#     )

#     # Payment method chart
#     payment_data = filtered_df["payment_method"].value_counts().reset_index()
#     payment_data.columns = ["payment_method", "count"]

#     payment_method_fig = go.Figure(data=[go.Pie(
#         labels=payment_data["payment_method"],
#         values=payment_data["count"],
#         hole=.4,
#         marker_colors=COLORS['chart_colors'],
#     )])
#     payment_method_fig.update_layout(
#         title="Payment Methods",
#         paper_bgcolor='rgba(0,0,0,0)',
#         showlegend=True,
#         margin=dict(l=0, r=0, t=40, b=0),
#     )

#     # Metrics
#     total_sales = f"${filtered_df['grand_total'].sum():,.2f}"
#     total_orders = f"{filtered_df['item_id'].nunique():,}"
#     avg_order_value = f"${filtered_df['grand_total'].mean():,.2f}" if not filtered_df.empty else "$0.00"

#     return sales_trend_fig, category_sales_fig, payment_method_fig, total_sales, total_orders, avg_order_value


# # Add Font Awesome to the app
# app.index_string = '''
# <!DOCTYPE html>
# <html>
#     <head>
#         {%metas%}
#         <title>{%title%}</title>
#         {%favicon%}
#         {%css%}
#         <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
#     </head>
#     <body>
#         {%app_entry%}
#         <footer>
#             {%config%}
#             {%scripts%}
#             {%renderer%}
#         </footer>
#     </body>
# </html>
# '''

# if __name__ == "__main__":
#     app.run_server(debug=True, port=8060)
