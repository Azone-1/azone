# telegram_service.py
# Telegram Bot Integration Service for AZone Bot Builder
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from bot_logic_engine import BotLogicEngine
import bot_db_manager

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBotService:
    """Service for managing Telegram bot connections"""
    
    def __init__(self, bot_token, bot_name):
        self.bot_token = bot_token
        self.bot_name = bot_name
        self.application = None
        self.is_running = False
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        try:
            # Check if bot still exists in database (might have been deleted)
            bot = bot_db_manager.get_bot_by_name(self.bot_name)
            if not bot:
                await update.message.reply_text("Bot has been deleted. This bot is no longer available.")
                # Stop this bot service
                self.stop()
                return
            
            user = update.effective_user
            chat_id = update.effective_chat.id
            
            # Initialize bot engine
            engine = BotLogicEngine(bot)
            
            # Initialize session
            session_data = {
                'current_step': None,
                'variables': {},
                'completed_steps': [],
                'telegram_user_id': user.id,
                'telegram_username': user.username,
                'telegram_chat_id': chat_id,
                'telegram_first_name': user.first_name,
                'telegram_last_name': user.last_name
            }
            
            # Get initial greeting
            initial_greeting = bot.get('initial_greeting', 'Hello! How can I help you?')
            
            # Send initial greeting
            await update.message.reply_text(initial_greeting)
            
            # Store session and engine
            context.user_data['session_data'] = session_data
            context.user_data['bot_engine'] = engine
            context.user_data['bot_config'] = bot
            
            logger.info(f"User {user.id} started conversation with bot {self.bot_name}")
            
        except Exception as e:
            logger.error(f"Error in start_command: {e}")
            await update.message.reply_text("Sorry, an error occurred. Please try again.")
        
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages"""
        try:
            # Check if bot still exists in database (might have been deleted)
            bot = bot_db_manager.get_bot_by_name(self.bot_name)
            if not bot:
                await update.message.reply_text("Bot has been deleted. This bot is no longer available.")
                # Stop this bot service
                self.stop()
                return
            
            user = update.effective_user
            user_message = update.message.text
            chat_id = update.effective_chat.id
            
            # Get or initialize session data
            session_data = context.user_data.get('session_data', {})
            engine = context.user_data.get('bot_engine')
            bot_config = context.user_data.get('bot_config')
            
            if not engine or not bot_config:
                # Initialize if not exists
                if not bot:
                    await update.message.reply_text("Bot configuration not found. Please contact administrator.")
                    return
                engine = BotLogicEngine(bot)
                context.user_data['bot_engine'] = engine
                context.user_data['bot_config'] = bot
                
                # Initialize session
                if not session_data:
                    session_data = {
                        'current_step': None,
                        'variables': {},
                        'completed_steps': [],
                        'telegram_user_id': user.id,
                        'telegram_username': user.username,
                        'telegram_chat_id': chat_id,
                        'telegram_first_name': user.first_name,
                        'telegram_last_name': user.last_name
                    }
            
            # Update session with user info
            session_data['telegram_user_id'] = user.id
            session_data['telegram_username'] = user.username
            session_data['telegram_chat_id'] = chat_id
            session_data['telegram_first_name'] = user.first_name
            session_data['telegram_last_name'] = user.last_name
            session_data['last_user_message'] = user_message
            
            # Process message through bot engine
            result = engine.process_message(user_message, session_data)
            
            bot_response = result.get('bot_response', '')
            new_session_data = result.get('session_data', {})
            
            # Update session
            context.user_data['session_data'] = new_session_data
            
            # Send response
            if bot_response:
                # Split long messages (Telegram has 4096 character limit)
                if len(bot_response) > 4096:
                    # Split into chunks
                    chunks = [bot_response[i:i+4096] for i in range(0, len(bot_response), 4096)]
                    for chunk in chunks:
                        await update.message.reply_text(chunk)
                else:
                    await update.message.reply_text(bot_response)
            else:
                await update.message.reply_text("I'm not sure how to respond. Please try again.")
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            import traceback
            traceback.print_exc()
            await update.message.reply_text("Sorry, an error occurred. Please try again.")
    
    def run(self):
        """Start the Telegram bot (polling mode)"""
        try:
            # Create application
            self.application = Application.builder().token(self.bot_token).build()
            
            # Add handlers
            self.application.add_handler(CommandHandler("start", self.start_command))
            self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
            
            # Mark as running
            self.is_running = True
            
            # Start bot
            logger.info(f"Starting Telegram bot: {self.bot_name}")
            self.application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
            
        except Exception as e:
            logger.error(f"Error starting Telegram bot: {e}")
            self.is_running = False
            raise
    
    def stop(self):
        """Stop the Telegram bot"""
        try:
            self.is_running = False
            if self.application:
                try:
                    # Stop the application (this will stop polling)
                    if hasattr(self.application, 'stop'):
                        self.application.stop()
                    if hasattr(self.application, 'shutdown'):
                        self.application.shutdown()
                    # Also try to stop updater if it exists
                    if hasattr(self.application, 'updater') and self.application.updater:
                        if hasattr(self.application.updater, 'stop'):
                            self.application.updater.stop()
                except Exception as app_error:
                    logger.warning(f"Error stopping application: {app_error}")
            logger.info(f"Stopped Telegram bot: {self.bot_name}")
        except Exception as e:
            logger.error(f"Error stopping Telegram bot: {e}")
            self.is_running = False
    
    async def set_webhook(self, webhook_url):
        """Set webhook URL for Telegram (for production)"""
        try:
            if self.application:
                await self.application.bot.set_webhook(url=webhook_url)
                logger.info(f"Webhook set to: {webhook_url}")
                return True
        except Exception as e:
            logger.error(f"Error setting webhook: {e}")
            return False

# Global dictionary to store running bots
telegram_bots = {}

def start_telegram_bot(bot_name, bot_token):
    """Start a Telegram bot for a specific bot configuration"""
    import threading
    
    if bot_name in telegram_bots:
        logger.warning(f"Bot {bot_name} is already running")
        return telegram_bots[bot_name]
    
    try:
        service = TelegramBotService(bot_token, bot_name)
        
        # Start in background thread
        def run_bot():
            try:
                service.run()
            except Exception as e:
                logger.error(f"Error in bot thread: {e}")
                service.is_running = False
                if bot_name in telegram_bots:
                    del telegram_bots[bot_name]
        
        thread = threading.Thread(target=run_bot, daemon=True)
        thread.start()
        
        # Wait a bit to check if it started successfully
        import time
        time.sleep(1)
        
        if service.is_running:
            telegram_bots[bot_name] = service
            logger.info(f"Telegram bot {bot_name} started successfully")
            return service
        else:
            logger.error(f"Failed to start Telegram bot {bot_name}")
            return None
            
    except Exception as e:
        logger.error(f"Error starting Telegram bot: {e}")
        return None

def stop_telegram_bot(bot_name):
    """Stop a Telegram bot"""
    if bot_name in telegram_bots:
        try:
            service = telegram_bots[bot_name]
            # Stop the service
            service.stop()
            # Remove from dictionary
            del telegram_bots[bot_name]
            logger.info(f"Stopped Telegram bot: {bot_name}")
            return True
        except Exception as e:
            logger.error(f"Error stopping Telegram bot: {e}")
            # Still remove from dictionary even if stop fails
            if bot_name in telegram_bots:
                del telegram_bots[bot_name]
            return False
    else:
        logger.warning(f"Telegram bot '{bot_name}' not found in running bots")
    return False

def get_telegram_bot_status(bot_name):
    """Get status of a Telegram bot"""
    if bot_name in telegram_bots:
        service = telegram_bots[bot_name]
        return {
            'running': service.is_running,
            'bot_name': bot_name
        }
    return {
        'running': False,
        'bot_name': bot_name
    }

