from dash import Input, Output, callback, no_update, html, State, ALL, MATCH, ctx
import pandas as pd
import plotly.graph_objects as go
from constants.generic_constants import CHART_TYPES, AGGREGATIONS, LIGHT_THEME, DARK_THEME, load_data
from components.create_graph_with_controls import create_graph_with_controls

def register_graph_management_callback(app):
    @app.callback(
        Output('graphs-container', 'children'),
        [Input('add-graph-button', 'n_clicks'),
         Input({'type': 'delete-button', 'index': ALL}, 'n_clicks')],
        State('graphs-container', 'children'),
        prevent_initial_call=True
    )
    def manage_graphs(add_clicks, delete_clicks, existing_children):
        triggered = ctx.triggered_id
        
        if existing_children is None:
            existing_children = []
            
        # Handle Add Graph button
        if triggered == 'add-graph-button':
            if add_clicks:
                new_id = f"graph-{len(existing_children) + 1}"
                existing_children.append(create_graph_with_controls(id_suffix=new_id))
            
        # Handle Delete button
        elif isinstance(triggered, dict) and triggered.get('type') == 'delete-button':
            deleted_index = triggered.get('index')
            existing_children = [
                child for child in existing_children 
                if child['props']['id']['index'] != deleted_index
            ]
            
        return existing_children
