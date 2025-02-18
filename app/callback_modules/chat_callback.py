from dash import Input, Output, callback, no_update, html, State, callback_context
import httpx
import logging
from components.chatbot import create_message_bubble, create_typing_indicator
from typing import List, Dict, Any

logging.basicConfig(level=logging.ERROR, filename="errors.log")

def register_chat_callback(app):
    @app.callback(
        [Output("chat-display", "children"),
         Output("user-input", "value"),
         Output("typing-indicator", "style")],
        [Input("send-button", "n_clicks"),
         Input("user-input", "n_submit")],
        [State("chat-display", "children"),
         State("user-input", "value")]
    )
    def update_chat(n_clicks, n_submit, current_messages, user_input):
        ctx = callback_context
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if not user_input or user_input.strip() == "":
            return no_update, no_update, {'display': 'none'}
        
        if current_messages is None:
            current_messages = []
        
        user_message = create_message_bubble(user_input, is_bot=False)
        
        typing_style = {'display': 'block'}
        current_messages_with_typing = current_messages + [user_message, create_typing_indicator()]
        
        try:
            response = fetch_chat_response(user_input)
            bot_response = response.get('response', "Sorry, I didn't get a valid response.")
            
            bot_message = create_message_bubble(bot_response, is_bot=True)
            
            updated_messages = current_messages + [user_message, bot_message]
            return updated_messages, "", {'display': 'none'}
        
        except Exception as e:
            logging.error(f"Error fetching chat response: {e}")
            error_message = create_message_bubble("Sorry, there was an error processing your request.", is_bot=True)
            
            updated_messages = current_messages + [user_message, error_message]
            return updated_messages, "", {'display': 'none'}

def fetch_chat_response(user_query: str) -> Dict[str, Any]:
    url = "http://127.0.0.1:8000/chat"
    payload = {"query": user_query}
    
    try:
        with httpx.Client() as client:
            response = client.post(url, json=payload, timeout=10)
            response.raise_for_status()  
            return response.json()
    except httpx.RequestError as e:
        logging.error(f"Network error: {e}")
        raise
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error: {e}")
        raise