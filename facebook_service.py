# facebook_service.py
# Facebook Messenger Integration Service for AZone Bot Builder
import os
import logging
import requests
import json
from bot_logic_engine import BotLogicEngine
import bot_db_manager

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Facebook Graph API base URL
GRAPH_API_URL = "https://graph.facebook.com/v18.0"

class FacebookBotService:
    """Service for managing Facebook Messenger bot connections"""
    
    def __init__(self, page_access_token, bot_name):
        self.page_access_token = page_access_token
        self.bot_name = bot_name
        self.is_running = False
        # Store user sessions (sender_id -> session_data)
        self.user_sessions = {}
    
    def verify_webhook(self, mode, token, challenge):
        """
        Verify webhook during Facebook setup
        Returns challenge if verification succeeds
        """
        verify_token = os.getenv('FACEBOOK_VERIFY_TOKEN', 'azone_bot_verify_token')
        
        if mode == 'subscribe' and token == verify_token:
            logger.info(f"Webhook verified for bot: {self.bot_name}")
            return challenge
        else:
            logger.warning(f"Webhook verification failed for bot: {self.bot_name}")
            return None
    
    def handle_message(self, sender_id, message_text):
        """
        Handle incoming message from Facebook Messenger
        Returns bot response
        """
        try:
            # Check if bot still exists in database
            bot = bot_db_manager.get_bot_by_name(self.bot_name)
            if not bot:
                return "Bot has been deleted. This bot is no longer available."
            
            # Get or initialize session data
            if sender_id not in self.user_sessions:
                # Initialize session for new user
                session_data = {
                    'current_step': None,
                    'variables': {},
                    'completed_steps': [],
                    'facebook_sender_id': sender_id,
                    'last_user_message': message_text
                }
                # Initialize bot engine
                engine = BotLogicEngine(bot)
                self.user_sessions[sender_id] = {
                    'session_data': session_data,
                    'engine': engine,
                    'bot_config': bot
                }
                
                # Send initial greeting
                initial_greeting = bot.get('initial_greeting', 'Hello! How can I help you?')
                self.send_message(sender_id, initial_greeting)
                return None  # Already sent greeting
            
            # Get existing session
            user_data = self.user_sessions[sender_id]
            session_data = user_data['session_data']
            engine = user_data['engine']
            
            # Update session with latest message
            session_data['last_user_message'] = message_text
            
            # Process message through bot engine
            result = engine.process_message(message_text, session_data)
            
            bot_response = result.get('bot_response', '')
            new_session_data = result.get('session_data', {})
            
            # Update session
            user_data['session_data'] = new_session_data
            
            # Send response
            if bot_response:
                self.send_message(sender_id, bot_response)
                return bot_response
            else:
                error_msg = "I'm not sure how to respond. Please try again."
                self.send_message(sender_id, error_msg)
                return error_msg
                
        except Exception as e:
            logger.error(f"Error processing Facebook message: {e}")
            import traceback
            traceback.print_exc()
            error_msg = "Sorry, an error occurred. Please try again."
            try:
                self.send_message(sender_id, error_msg)
            except:
                pass
            return error_msg
    
    def send_message(self, sender_id, message_text):
        """
        Send message to Facebook user via Graph API
        """
        try:
            url = f"{GRAPH_API_URL}/me/messages"
            params = {
                "access_token": self.page_access_token
            }
            payload = {
                "recipient": {"id": sender_id},
                "message": {"text": message_text}
            }
            
            # Facebook has 2000 character limit per message
            if len(message_text) > 2000:
                # Split into chunks
                chunks = [message_text[i:i+2000] for i in range(0, len(message_text), 2000)]
                for chunk in chunks:
                    payload["message"]["text"] = chunk
                    response = requests.post(url, params=params, json=payload)
                    if response.status_code != 200:
                        logger.error(f"Error sending Facebook message: {response.text}")
            else:
                response = requests.post(url, params=params, json=payload)
                if response.status_code == 200:
                    logger.info(f"Message sent to Facebook user {sender_id}")
                else:
                    logger.error(f"Error sending Facebook message: {response.text}")
                    raise Exception(f"Facebook API error: {response.text}")
                    
        except Exception as e:
            logger.error(f"Error in send_message: {e}")
            raise
    
    def send_typing_indicator(self, sender_id, is_typing=True):
        """
        Send typing indicator to user
        """
        try:
            url = f"{GRAPH_API_URL}/me/messages"
            params = {
                "access_token": self.page_access_token
            }
            action = "typing_on" if is_typing else "typing_off"
            payload = {
                "recipient": {"id": sender_id},
                "sender_action": action
            }
            
            response = requests.post(url, params=params, json=payload)
            if response.status_code != 200:
                logger.warning(f"Error sending typing indicator: {response.text}")
                
        except Exception as e:
            logger.warning(f"Error in send_typing_indicator: {e}")
    
    def process_webhook_event(self, event):
        """
        Process webhook event from Facebook
        """
        try:
            if event.get('message'):
                message = event['message']
                sender_id = event['sender']['id']
                message_text = message.get('text', '')
                
                if message_text:
                    # Send typing indicator
                    self.send_typing_indicator(sender_id, True)
                    
                    # Process message
                    self.handle_message(sender_id, message_text)
                    
                    # Stop typing indicator
                    self.send_typing_indicator(sender_id, False)
                    
        except Exception as e:
            logger.error(f"Error processing webhook event: {e}")
            import traceback
            traceback.print_exc()
    
    def stop(self):
        """Stop the Facebook bot service"""
        try:
            self.is_running = False
            self.user_sessions.clear()
            logger.info(f"Stopped Facebook bot: {self.bot_name}")
        except Exception as e:
            logger.error(f"Error stopping Facebook bot: {e}")
            self.is_running = False

# Global dictionary to store running bots
facebook_bots = {}

def start_facebook_bot(bot_name, page_access_token):
    """Start a Facebook Messenger bot for a specific bot configuration"""
    if bot_name in facebook_bots:
        logger.warning(f"Facebook bot {bot_name} is already running")
        return facebook_bots[bot_name]
    
    try:
        service = FacebookBotService(page_access_token, bot_name)
        service.is_running = True
        facebook_bots[bot_name] = service
        logger.info(f"Facebook bot {bot_name} started successfully")
        return service
    except Exception as e:
        logger.error(f"Error starting Facebook bot: {e}")
        return None

def stop_facebook_bot(bot_name):
    """Stop a Facebook Messenger bot"""
    if bot_name in facebook_bots:
        try:
            service = facebook_bots[bot_name]
            service.stop()
            del facebook_bots[bot_name]
            logger.info(f"Stopped Facebook bot: {bot_name}")
            return True
        except Exception as e:
            logger.error(f"Error stopping Facebook bot: {e}")
            if bot_name in facebook_bots:
                del facebook_bots[bot_name]
            return False
    else:
        logger.warning(f"Facebook bot '{bot_name}' not found in running bots")
    return False

def get_facebook_bot_status(bot_name):
    """Get status of a Facebook Messenger bot"""
    if bot_name in facebook_bots:
        service = facebook_bots[bot_name]
        return {
            'running': service.is_running,
            'bot_name': bot_name
        }
    return {
        'running': False,
        'bot_name': bot_name
    }

def get_facebook_bot_service(bot_name):
    """Get Facebook bot service instance"""
    return facebook_bots.get(bot_name)

