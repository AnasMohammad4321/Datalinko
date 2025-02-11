from dash import Input, Output, callback, no_update, html, State, callback_context
import httpx
import logging
import asyncio
from app.components.chatbot import create_message_bubble, create_typing_indicator
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
    def handle_chat_interaction(n_clicks, n_submit, current_messages, user_input):
        ctx = callback_context
        if not ctx.triggered:
            return no_update, no_update, {'display': 'none'}

        if not user_input or user_input.strip() == "":
            return no_update, no_update, {'display': 'none'}

        if current_messages is None:
            current_messages = []

        user_message = create_message_bubble(user_input, is_bot=False)
        updated_messages = current_messages + [user_message]

        # typing_style = show_typing_indicator()
        typing_style = ""

        bot_response = asyncio.run(get_bot_response(user_input)) 

        updated_messages.append(bot_response)

        return updated_messages, "", typing_style

def show_typing_indicator() -> Dict[str, str]:
    return {'display': 'flex', 'maxWidth': '80px', 'alignItems': 'center'}

async def get_bot_response(user_input: str) -> Any:
    """ Fetch bot response asynchronously """
    try:
        response = await fetch_chat_response(user_input)
        bot_response = response.get('response', "Sorry, I didn't get a valid response.")
        return create_message_bubble(bot_response, is_bot=True)
    except Exception as e:
        logging.error(f"Error fetching chat response: {e}")
        return create_message_bubble("Sorry, there was an error processing your request.", is_bot=True)

async def fetch_chat_response(user_query: str) -> Dict[str, Any]:
    """ Make an asynchronous HTTP request to fetch chat response """
    url = "http://127.0.0.1:8000/chat"
    payload = {"query": user_query}

    try:
        async with httpx.AsyncClient() as client:  
            response = await client.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        logging.error(f"Network error: {e}")
        return {"response": "I'm unable to connect to the server right now."}
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error: {e}")
        return {"response": "There was an issue with the server response."}




# from dash import Input, Output, callback, no_update, html, State, callback_context
# import httpx
# import logging
# from app.components.chatbot import create_message_bubble, create_typing_indicator
# from typing import List, Dict, Any

# logging.basicConfig(level=logging.ERROR, filename="errors.log")

# def register_chat_callback(app):
#     @app.callback(
#         [Output("chat-display", "children"),
#          Output("user-input", "value"),
#          Output("typing-indicator", "style")],
#         [Input("send-button", "n_clicks"),
#          Input("user-input", "n_submit")],
#         [State("chat-display", "children"),
#          State("user-input", "value")]
#     )
#     def update_chat(n_clicks, n_submit, current_messages, user_input):
#         # Trigger on either button click or enter key
#         ctx = callback_context
#         trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
#         # Check if input is empty
#         if not user_input or user_input.strip() == "":
#             return no_update, no_update, {'display': 'none'}
        
#         # Initialize messages list if None
#         if current_messages is None:
#             current_messages = []
        
#         # Create user message bubble
#         user_message = create_message_bubble(user_input, is_bot=False)
        
#         # Show typing indicator immediately
#         typing_style = {'display': 'block'}
#         current_messages_with_typing = current_messages + [user_message, create_typing_indicator()]
        
#         try:
#             # Fetch response (this will block, consider async in production)
#             response = fetch_chat_response(user_input)
#             bot_response = response.get('response', "Sorry, I didn't get a valid response.")
            
#             # Create bot message bubble
#             bot_message = create_message_bubble(bot_response, is_bot=True)
            
#             # Update messages, clear input, hide typing indicator
#             updated_messages = current_messages + [user_message, bot_message]
#             return updated_messages, "", {'display': 'none'}
        
#         except Exception as e:
#             logging.error(f"Error fetching chat response: {e}")
#             error_message = create_message_bubble("Sorry, there was an error processing your request.", is_bot=True)
            
#             # Update messages, clear input, hide typing indicator
#             updated_messages = current_messages + [user_message, error_message]
#             return updated_messages, "", {'display': 'none'}

# def fetch_chat_response(user_query: str) -> Dict[str, Any]:
#     url = "http://127.0.0.1:8000/chat"
#     payload = {"query": user_query}
    
#     try:
#         with httpx.Client() as client:
#             response = client.post(url, json=payload, timeout=10)
#             response.raise_for_status()  
#             return response.json()
#     except httpx.RequestError as e:
#         logging.error(f"Network error: {e}")
#         raise
#     except httpx.HTTPStatusError as e:
#         logging.error(f"HTTP error: {e}")
#         raise