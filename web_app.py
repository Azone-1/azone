# web_app.py (UPDATED)
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, abort, Response
from urllib.parse import unquote_plus
import db_manager
import bot_db_manager
import bot_logic_engine
import bot_templates
import gemini_service
import json
import uuid
import os
from datetime import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    current_user,
    login_required,
)
import auth_manager
from auth_routes import auth_bp
from session_middleware import check_session_timeout, cleanup_expired_sessions_periodically
import threading
import logging

logger = logging.getLogger(__name__)

# Telegram integration (optional - only import if available)
try:
    from telegram_service import start_telegram_bot, stop_telegram_bot, get_telegram_bot_status, telegram_bots
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    print("Warning: python-telegram-bot not installed. Telegram integration disabled.")

# Facebook Messenger integration (optional - only import if available)
try:
    from facebook_service import start_facebook_bot, stop_facebook_bot, get_facebook_bot_status, get_facebook_bot_service, facebook_bots
    FACEBOOK_AVAILABLE = True
except ImportError:
    FACEBOOK_AVAILABLE = False
    print("Warning: Facebook integration disabled.")

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
# Use secret key from config (which loads from .env file if available)
try:
    import config
    app.secret_key = config.Config.SECRET_KEY
except ImportError:
    app.secret_key = 'your-secret-key-here-change-in-production'  # Fallback if config not available

# Flask-Login configuration
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'ကျေးဇူးပြု၍ ပထမဦးစွာ login ဝင်ပါ။'
login_manager.init_app(app)

# Simple user model for Flask-Login
class AppUser(UserMixin):
    def __init__(self, user_data):
        self.id = user_data['id']
        self.username = user_data.get('username')
        self.email = user_data.get('email')
        self.role = user_data.get('role', 'viewer')

    def get_id(self):
        return str(self.id)


@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login"""
    # Check session timeout first
    if not check_session_timeout():
        return None
    
    # Try auth_manager first, fallback to bot_db_manager
    user = auth_manager.get_user_by_id(user_id)
    if not user:
        user = bot_db_manager.get_user_by_id(user_id)
    
    if user:
        return AppUser(user)
    return None

# Initialize databases on startup
db_manager.init_database()
bot_db_manager.init_bot_database()
auth_manager.init_auth_database()  # Initialize auth database

# Import and initialize API templates
try:
    from api_templates import (
        init_api_templates,
        get_leads_template,
        create_lead_template,
        update_lead_template,
        delete_lead_template,
        get_customers_template,
        create_customer_template,
        get_projects_template,
        create_project_template,
        update_project_status_template,
        get_dashboard_stats_template,
        get_dashboard_chart_data_template
    )
    
    # Initialize API templates with app instance
    init_api_templates(app)
    
    # Register API routes
    get_leads_template()
    create_lead_template()
    update_lead_template()
    delete_lead_template()
    get_customers_template()
    create_customer_template()
    get_projects_template()
    create_project_template()
    update_project_status_template()
    get_dashboard_stats_template()
    get_dashboard_chart_data_template()
    
    print("API templates initialized and routes registered")
except Exception as e:
    print(f"Warning: Could not initialize API templates: {e}")

# Register authentication blueprint
app.register_blueprint(auth_bp, url_prefix='')

# Cleanup expired sessions on startup
cleanup_expired_sessions_periodically()

def role_required(*roles):
    """Decorator to enforce role-based authorization."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('ကျေးဇူးပြု၍ ပထမဦးစွာ login ဝင်ပါ။', 'error')
                return redirect(url_for('login', next=request.path))
            if current_user.role not in roles:
                abort(403)
            return view_func(*args, **kwargs)
        return wrapper
    return decorator

def get_webhook_url():
    """
    Get the webhook URL for Facebook Messenger.
    Uses domain from config if available, otherwise falls back to request URL.
    """
    try:
        import config
        domain = config.Config.DOMAIN
        use_https = config.Config.USE_HTTPS
        
        if domain:
            protocol = 'https' if use_https else 'http'
            return f"{protocol}://{domain}/webhook/facebook"
        else:
            # Fallback to request URL
            return f"{request.url_root.rstrip('/')}/webhook/facebook"
    except:
        # Fallback to request URL if config fails
        return f"{request.url_root.rstrip('/')}/webhook/facebook"

@app.context_processor
def inject_user():
    """Inject current user info for templates."""
    return {
        'current_user': current_user if current_user.is_authenticated else None,
        'get_webhook_url': get_webhook_url
    }

@app.route('/')
def index():
    """Main Dashboard Page - CRM Dashboard"""
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    # Show CRM Dashboard (index.html)
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """CRM Dashboard Page"""
    return render_template('index.html')

@app.route('/crm')
@login_required
def crm_dashboard():
    """CRM Dashboard Page (alternative route)"""
    return render_template('index.html')

@app.route('/bot-builder')
@login_required
def bot_builder():
    """Bot Builder UI Page"""
    # Check if bot_name parameter is provided (for editing)
    bot_name = request.args.get('bot_name', '').strip()
    use_draft = request.args.get('draft', 'false').lower() == 'true'
    bot_data = None
    draft_data = None
    live_data = None
    versions = []
    
    if bot_name:
        # Load draft version if requested, otherwise load live
        if use_draft:
            bot_data = bot_db_manager.get_bot_draft_version(bot_name)
            if not bot_data:
                flash(f'Draft version of bot "{bot_name}" not found', 'error')
        else:
            bot_data = bot_db_manager.get_bot_by_name(bot_name, use_draft=False)
            if not bot_data:
                flash(f'Bot "{bot_name}" not found', 'error')
        
        # Get both draft and live versions for status display
        draft_data = bot_db_manager.get_bot_draft_version(bot_name)
        live_data = bot_db_manager.get_bot_live_version(bot_name)
        versions = bot_db_manager.get_bot_versions(bot_name)
    
    # Pass active_menu and bot_data to template
    try:
        templates = bot_templates.list_templates() or []
    except Exception as e:
        print(f"Error loading templates in bot_builder: {e}")
        templates = []
    return render_template('dashboard.html', templates=templates,  
                         active_menu='bot-builder', 
                         bot_data=bot_data,
                         draft_data=draft_data,
                         live_data=live_data,
                         versions=versions)

@app.route('/analytics')
@login_required
def analytics():
    """Analytics UI Page"""
    # Get analytics data
    days = int(request.args.get('days', 30))
    bot_id = request.args.get('bot_id', type=int)
    
    all_stats = bot_db_manager.get_conversation_stats(bot_id=bot_id, days=days)
    bots = bot_db_manager.get_all_bots()
    
    # Get detailed analytics for each bot
    bot_analytics = {}
    step_analytics = {}
    for bot in bots:
        analytics_data = bot_db_manager.get_bot_analytics(bot['id'], days=days)
        bot_analytics[bot['bot_name']] = analytics_data
        
        # Get step-level analytics
        step_data = bot_db_manager.get_step_analytics(bot['id'], days=days)
        step_analytics[bot['bot_name']] = step_data
    
    try:
        templates = bot_templates.list_templates() or []
    except Exception as e:
        print(f"Error loading templates in analytics: {e}")
        templates = []
    return render_template('dashboard.html', templates=templates,  
                         active_menu='analytics', 
                         stats=all_stats,
                         bot_analytics=bot_analytics,
                         step_analytics=step_analytics,
                         selected_days=days,
                         selected_bot_id=bot_id)

@app.route('/my-bots')
@login_required
def my_bots():
    """My Bots List Page"""
    # Fetch all bots from database
    user_id = current_user.id if current_user.is_authenticated else None
    role = current_user.role if current_user.is_authenticated else 'viewer'
    bots = bot_db_manager.get_all_bots(user_id=user_id, role=role)
    # Pass active_menu and bots list to template
    try:
        templates = bot_templates.list_templates() or []
    except Exception as e:
        print(f"Error loading templates in my_bots: {e}")
        templates = []
    return render_template('dashboard.html', templates=templates, active_menu='my-bots', bots=bots)

@app.route('/templates')
@login_required
def templates_page():
    """Templates Library Page"""
    try:
        templates = bot_templates.list_templates() or []
    except Exception as e:
        print(f"Error loading templates in templates_page: {e}")
        templates = []
    return render_template('dashboard.html', templates=templates, active_menu='templates')

@app.route('/gemini-chat')
@login_required
def gemini_chat_page():
    """Gemini AI Chat Page"""
    # Check if Gemini is available
    gemini_available = gemini_service.GeminiService.is_available()
    try:
        templates = bot_templates.list_templates() or []
    except Exception as e:
        print(f"Error loading templates in gemini_chat_page: {e}")
        templates = []
    return render_template('dashboard.html', templates=templates, active_menu='gemini-chat', gemini_available=gemini_available)

@app.route('/api/bot/delete/<bot_name>', methods=['DELETE', 'POST'])
@login_required
@role_required('owner', 'editor')
def delete_bot(bot_name):
    """Delete a bot from the database and disconnect Telegram if connected"""
    try:
        # Decode URL-encoded bot name
        bot_name = unquote_plus(bot_name)
        bot_name = bot_name.replace('%20', ' ')
        
        # Stop Telegram connection if exists (BEFORE deleting from database)
        if TELEGRAM_AVAILABLE:
            try:
                stop_telegram_bot(bot_name)
                print(f"Telegram bot '{bot_name}' disconnected before deletion")
            except Exception as tg_error:
                print(f"Warning: Error disconnecting Telegram bot '{bot_name}': {tg_error}")
                # Continue with deletion even if Telegram disconnect fails
        
        # Delete the bot from database
        success = bot_db_manager.delete_bot(bot_name)
        
        if success:
            platforms_stopped = []
            if TELEGRAM_AVAILABLE and bot_name in telegram_bots:
                platforms_stopped.append('Telegram')
            if FACEBOOK_AVAILABLE and bot_name in facebook_bots:
                platforms_stopped.append('Facebook')
            
            message = f'Bot "{bot_name}" deleted successfully.'
            if platforms_stopped:
                message += f' Platform connections stopped: {", ".join(platforms_stopped)}.'
            
            return jsonify({
                'success': True,
                'message': message
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f'Bot "{bot_name}" not found'
            }), 404
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error deleting bot: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/save-bot', methods=['POST'])
@login_required
def save_bot():
    """
    Handle bot configuration form submission
    Saves or updates bot data in the database
    """
    try:
        # Get form data - handle both JSON and form data
        print(f"Request method: {request.method}")
        print(f"Content-Type: {request.content_type}")
        print(f"Is JSON: {request.is_json}")
        print(f"Form data: {dict(request.form)}")
        print(f"JSON data: {request.get_json(silent=True)}")
        
        if request.is_json or (request.content_type and 'application/json' in request.content_type):
            data = request.get_json(silent=True) or {}
            print("Using JSON data")
        else:
            data = request.form.to_dict()
            print("Using form data")
        
        # Debug: Log incoming data
        print(f"Received data type: {type(data)}")
        print(f"Received data: {data}")
        
        # Extract data with multiple possible key names
        bot_name = (data.get('botName') or data.get('bot_name') or '').strip()
        initial_greeting = (data.get('initialGreeting') or data.get('initial_greeting') or '').strip()
        steps_json = data.get('stepsJson') or data.get('steps_json') or '[]'
        
        # Validate required fields
        if not bot_name:
            error_msg = 'Bot name is required. Please enter a bot name.'
            print("Error: Bot name is missing")
            if request.is_json or (request.content_type and 'application/json' in request.content_type):
                return jsonify({'success': False, 'error': error_msg}), 400
            flash(error_msg, 'error')
            return redirect(url_for('bot_builder'))
        
        if not initial_greeting:
            error_msg = 'Initial greeting is required. Please enter an initial greeting message.'
            print("Error: Initial greeting is missing")
            if request.is_json or (request.content_type and 'application/json' in request.content_type):
                return jsonify({'success': False, 'error': error_msg}), 400
            flash(error_msg, 'error')
            return redirect(url_for('bot_builder'))
        
        # Parse steps JSON
        steps_data = []
        try:
            if isinstance(steps_json, str):
                steps_data = json.loads(steps_json)
            elif isinstance(steps_json, list):
                steps_data = steps_json
            else:
                steps_data = []
            
            if not isinstance(steps_data, list):
                steps_data = []
                flash('Warning: Steps data format is invalid. Bot saved without steps.', 'warning')
        except json.JSONDecodeError as e:
            steps_data = []
            flash(f'Warning: Invalid steps JSON format: {str(e)}. Bot saved without steps.', 'warning')
            print(f"JSON decode error: {e}")
        
        print(f"Bot Name: {bot_name}")
        print(f"Initial Greeting: {initial_greeting[:50]}...")
        print(f"Steps Count: {len(steps_data)}")
        
        # Check if publish is requested
        publish_val = data.get('publish', 'false')
        if isinstance(publish_val, str):
            publish = publish_val.lower() == 'true'
        else:
            publish = bool(publish_val)
        
        # Save bot to database
        print("Calling bot_db_manager.save_bot()...")
        success, message, bot_id = bot_db_manager.save_bot(
            bot_name=bot_name,
            initial_greeting=initial_greeting,
            steps_data=steps_data,
            owner_id=current_user.id if current_user.is_authenticated else None,
            publish=publish
        )
        print(f"Save result - Success: {success}, Message: {message}, Bot ID: {bot_id}")
        
        # Check if request is JSON (from Fetch API) or form submission
        if request.is_json or (request.content_type and 'application/json' in request.content_type):
            # Return JSON response for Fetch API
            if success:
                return jsonify({
                    'success': True,
                    'message': f'Bot "{bot_name}" has been saved successfully!',
                    'bot_id': bot_id
                }), 200
            else:
                # Handle specific error cases
                # Ensure message is a string before calling .lower()
                message_str = str(message) if message is not None else 'Unknown error'
                if 'already exists' in message_str.lower() or 'unique' in message_str.lower():
                    error_msg = f'Bot name "{bot_name}" already exists. Please use a different name.'
                else:
                    error_msg = message_str
                return jsonify({
                    'success': False,
                    'error': error_msg
                }), 400
        else:
            # Traditional form submission - use flash messages and redirect
            if success:
                flash(f'Bot "{bot_name}" has been saved successfully!', 'success')
                print(f"Success: {message}")
            else:
                # Handle specific error cases
                # Ensure message is a string before calling .lower()
                message_str = str(message) if message is not None else 'Unknown error'
                if 'already exists' in message_str.lower() or 'unique' in message_str.lower():
                    flash(f'Error: Bot name "{bot_name}" already exists. Please use a different name.', 'error')
                else:
                    flash(f'Error: {message_str}', 'error')
                print(f"Error: {message_str}")
            
            # Redirect back to bot builder
            return redirect(url_for('bot_builder'))
        
    except json.JSONDecodeError as e:
        error_msg = f'Invalid JSON data format: {str(e)}'
        print(f"JSON Error: {error_msg}")
        # Check if request is JSON (from Fetch API) or form submission
        if request.is_json or (request.content_type and 'application/json' in request.content_type):
            return jsonify({
                'success': False,
                'error': error_msg
            }), 400
        flash(error_msg, 'error')
        return redirect(url_for('bot_builder'))
    except Exception as e:
        error_msg = f'Error saving bot: {str(e)}'
        print(f"Exception: {error_msg}")
        import traceback
        traceback.print_exc()
        # Check if request is JSON (from Fetch API) or form submission
        if request.is_json or (request.content_type and 'application/json' in request.content_type):
            return jsonify({
                'success': False,
                'error': error_msg
            }), 500
        flash(error_msg, 'error')
        return redirect(url_for('bot_builder'))

@app.route('/publish-bot', methods=['POST'])
@login_required
def publish_bot():
    """
    Publish a draft bot (promote draft to published)
    """
    try:
        # Get bot name from request
        if request.is_json or (request.content_type and 'application/json' in request.content_type):
            data = request.get_json(silent=True) or {}
        else:
            data = request.form.to_dict()
        
        bot_name = (data.get('botName') or data.get('bot_name') or '').strip()
        
        if not bot_name:
            error_msg = 'Bot name is required.'
            if request.is_json or (request.content_type and 'application/json' in request.content_type):
                return jsonify({'success': False, 'error': error_msg}), 400
            flash(error_msg, 'error')
            return redirect(url_for('bot_builder'))
        
        # Publish the bot
        success, message = bot_db_manager.publish_draft(
            bot_name=bot_name,
            owner_id=current_user.id if current_user.is_authenticated else None
        )
        
        if success:
            if request.is_json or (request.content_type and 'application/json' in request.content_type):
                return jsonify({
                    'success': True,
                    'message': f'Bot "{bot_name}" has been published successfully!'
                }), 200
            flash(f'Bot "{bot_name}" has been published successfully!', 'success')
        else:
            if request.is_json or (request.content_type and 'application/json' in request.content_type):
                return jsonify({
                    'success': False,
                    'error': message
                }), 400
            flash(f'Error: {message}', 'error')
        
        return redirect(url_for('bot_builder'))
        
    except Exception as e:
        error_msg = f'Error publishing bot: {str(e)}'
        print(f"Exception: {error_msg}")
        import traceback
        traceback.print_exc()
        if request.is_json or (request.content_type and 'application/json' in request.content_type):
            return jsonify({
                'success': False,
                'error': error_msg
            }), 500
        flash(error_msg, 'error')
        return redirect(url_for('bot_builder'))

@app.route('/chat', methods=['POST'])
def chat():
    """
    Advanced Chatbot API Endpoint
    Uses BotLogicEngine for intelligent conversation handling
    """
    try:
        # Get JSON data from request
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 400
        
        data = request.get_json()
        bot_name = data.get('bot_name', '').strip()
        user_message = data.get('user_message', '').strip()
        session_data = data.get('session_data', {})
        session_id = data.get('session_id') or str(uuid.uuid4())
        
        # Validate required fields
        if not bot_name:
            return jsonify({
                'success': False,
                'error': 'bot_name is required'
            }), 400
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'user_message is required'
            }), 400
        
        # Get bot configuration from database
        bot = bot_db_manager.get_bot_by_name(bot_name)
        if not bot:
            return jsonify({
                'success': False,
                'error': f'Bot "{bot_name}" not found'
            }), 404
        
        # Initialize Bot Logic Engine
        engine = bot_logic_engine.BotLogicEngine(bot)
        
        # Process message using advanced engine
        start_time = datetime.now()
        result = engine.process_message(user_message, session_data)
        end_time = datetime.now()
        
        response_time = (end_time - start_time).total_seconds()
        
        bot_response = result.get('bot_response', '')
        new_session_data = result.get('session_data', {})
        intent = result.get('intent', 'unknown')
        confidence = result.get('confidence', 0.0)
        step_index = result.get('step_index')
        step_type = result.get('step_type')
        api_latency = result.get('api_latency')
        
        # Log conversation for analytics
        bot_db_manager.log_conversation(
            bot_id=bot['id'],
            bot_name=bot_name,
            user_message=user_message,
            bot_response=bot_response,
            session_id=session_id,
            step_index=step_index,
            step_type=step_type,
            intent=intent,
            confidence=confidence,
            api_latency=api_latency
        )
        
        return jsonify({
            'success': True,
            'bot_response': bot_response,
            'session_data': new_session_data,
            'session_id': session_id,
            'intent': intent,
            'confidence': confidence,
            'step_index': step_index,
            'response_time': response_time
        }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Error processing chat: {str(e)}'
        }), 500

@app.route('/schedule', methods=['POST'])
@login_required
def schedule():
    """
    Handle form submission for scheduling a new post
    Inserts the post into the database
    """
    try:
        # Get form data
        data = request.get_json() if request.is_json else request.form
        
        content = data.get('content', '').strip()
        schedule_time = data.get('schedule_time', '').strip()
        platforms = data.get('platforms', '').strip()
        status = data.get('status', 'pending').strip()
        
        # Validate required fields
        if not content:
            return jsonify({'success': False, 'error': 'Content is required'}), 400
        if not schedule_time:
            return jsonify({'success': False, 'error': 'Schedule time is required'}), 400
        if not platforms:
            return jsonify({'success': False, 'error': 'Platforms are required'}), 400
        
        # Insert into database
        post_id = db_manager.insert_scheduled_post(
            content=content,
            schedule_time=schedule_time,
            platforms=platforms,
            status=status
        )
        
        return jsonify({
            'success': True,
            'message': 'Post scheduled successfully',
            'post_id': post_id
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error scheduling post: {str(e)}'
        }), 500 

@app.route('/api/analytics/stats', methods=['GET'])
def api_analytics_stats():
    """API endpoint for analytics statistics"""
    try:
        days = int(request.args.get('days', 30))
        bot_id = request.args.get('bot_id', type=int)
        
        if bot_id:
            stats = bot_db_manager.get_conversation_stats(bot_id=bot_id, days=days)
            analytics = bot_db_manager.get_bot_analytics(bot_id, days=days)
            step_analytics = bot_db_manager.get_step_analytics(bot_id, days=days)
        else:
            stats = bot_db_manager.get_conversation_stats(days=days)
            analytics = []
            step_analytics = []
        
        return jsonify({
            'success': True,
            'stats': stats,
            'analytics': analytics,
            'step_analytics': step_analytics
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/analytics/export', methods=['GET'])
@login_required
def export_analytics():
    """Export analytics data as CSV"""
    try:
        bot_id = request.args.get('bot_id', type=int)
        days = int(request.args.get('days', 30))
        format_type = request.args.get('format', 'csv').lower()
        
        if format_type == 'csv':
            csv_data = bot_db_manager.export_analytics_csv(bot_id=bot_id, days=days)
            if csv_data:
                from flask import Response
                return Response(
                    csv_data,
                    mimetype='text/csv',
                    headers={'Content-Disposition': f'attachment; filename=analytics_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'}
                )
            else:
                return jsonify({
                    'success': False,
                    'error': 'No data to export'
                }), 404
        elif format_type == 'json':
            # Export as JSON
            if bot_id:
                stats = bot_db_manager.get_conversation_stats(bot_id=bot_id, days=days)
                analytics = bot_db_manager.get_bot_analytics(bot_id, days=days)
                step_analytics = bot_db_manager.get_step_analytics(bot_id, days=days)
            else:
                stats = bot_db_manager.get_conversation_stats(days=days)
                analytics = []
                step_analytics = []
            
            export_data = {
                'export_date': datetime.now().isoformat(),
                'period_days': days,
                'stats': stats,
                'analytics': analytics,
                'step_analytics': step_analytics
            }
            
            from flask import Response
            return Response(
                json.dumps(export_data, indent=2, ensure_ascii=False),
                mimetype='application/json',
                headers={'Content-Disposition': f'attachment; filename=analytics_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'}
            )
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid format. Use "csv" or "json"'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/bot/export/<bot_name>', methods=['GET'])
@login_required
def export_bot(bot_name):
    bot_name = unquote_plus(bot_name)
    """Export bot configuration as JSON"""
    try:
        bot = bot_db_manager.get_bot_by_name(bot_name)
        if not bot:
            return jsonify({
                'success': False,
                'error': f'Bot "{bot_name}" not found'
            }), 404
        
        export_data = {
            'bot_name': bot['bot_name'],
            'initial_greeting': bot['initial_greeting'],
            'steps': bot['steps'],
            'exported_at': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'bot_config': export_data
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/bot/import', methods=['POST'])
@login_required
def import_bot():
    """Import bot configuration from JSON"""
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 400
        
        data = request.get_json()
        bot_config = data.get('bot_config', {})
        
        # Remove old bot_id if it exists (to ensure it's saved as a new bot)
        if 'bot_id' in bot_config:
            del bot_config['bot_id']
        if 'id' in bot_config:
            del bot_config['id']
        
        # Get bot name and add '[Imported] ' prefix
        original_bot_name = bot_config.get('bot_name', '').strip()
        if not original_bot_name:
            return jsonify({
                'success': False,
                'error': 'Bot name is required'
            }), 400
        
        # Add '[Imported] ' prefix to bot name
        bot_name = '[Imported] ' + original_bot_name
        initial_greeting = bot_config.get('initial_greeting', '')
        steps = bot_config.get('steps', [])
        
        # Save as a new bot (will create new entry even if name exists)
        success, message, bot_id = bot_db_manager.save_bot(
            bot_name=bot_name,
            initial_greeting=initial_greeting,
            steps_data=steps
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Bot "{bot_name}" imported successfully',
                'bot_id': bot_id
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': message
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login view."""
    if current_user.is_authenticated:
        return redirect(url_for('bot_builder'))
    
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        remember = request.form.get('remember') == 'on'
        
        user = bot_db_manager.get_user_by_username(username)

        # DEBUG: log login attempt
        print(f'[LOGIN DEBUG] submitted username/email: {username!r}')
        attempted_email_fallback = False
        if not user and '@' in username:
            attempted_email_fallback = True
            print('[LOGIN DEBUG] attempting lookup by email')
            user = bot_db_manager.get_user_by_email(username)

        if not user and "@" in username:
            user = bot_db_manager.get_user_by_email(username)
        if user and check_password_hash(user['password_hash'], password):
            login_user(AppUser(user), remember=remember)
            flash('Login အောင်မြင်ပါသည်။', 'success')
            next_url = request.args.get('next') or url_for('dashboard')
            return redirect(next_url)
        else:
            error = 'Username သို့မဟုတ် Password မမှန်ပါ။'
    
    return render_template('login.html', mode='login', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration view."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', 'viewer')
        
        if not username or not email or not password:
            flash('အချက်အလက်များကို ပြည့်စုံရေးပါ။', 'error')
            return render_template('login.html', mode='register')
        
        # Restrict elevated role creation to owners
        if role in ['owner', 'editor']:
            if not current_user.is_authenticated or current_user.role != 'owner':
                role = 'viewer'
        
        password_hash = generate_password_hash(password)
        success, user_id, error_message = bot_db_manager.create_user(
            username=username,
            email=email,
            password_hash=password_hash,
            role=role
        )
        
        if success:
            flash('အကောင့်အသစ် ဖန်တီးပြီးပါပြီ။ Login ဝင်ပါ။', 'success')
            return redirect(url_for('login'))
        else:
            flash(error_message or 'အကောင့် ဖန်တီးရာတွင် ပြဿနာရှိသည်။', 'error')
    
    return render_template('login.html', mode='register')

@app.route('/logout')
@login_required
def logout():
    """Logout current user."""
    logout_user()
    session.clear()
    flash('ထွက်ခွါပြီးပါပြီ။', 'success')
    return redirect(url_for('login'))

@app.route('/users')
@login_required
@role_required('owner')
def user_management():
    """User management view for owners."""
    users = bot_db_manager.list_users()
    try:
        templates = bot_templates.list_templates() or []
    except Exception as e:
        print(f"Error loading templates in user_management: {e}")
        templates = []
    return render_template('dashboard.html', templates=templates, active_menu='users', users=users)

@app.route('/users/update-role', methods=['POST'])
@login_required
@role_required('owner')
def update_user_role():
    """Update a user's role."""
    user_id = request.form.get('user_id', type=int)
    role = request.form.get('role', 'viewer')
    
    if not user_id:
        flash('User ID မရှိပါ။', 'error')
        return redirect(url_for('user_management'))
    
    if bot_db_manager.update_user_role(user_id, role):
        flash('Role ကို အောင်မြင်စွာ ပြင်ဆင်လိုက်ပါပြီ။', 'success')
    else:
        flash('Role ပြင်ရန် မအောင်မြင်ပါ။', 'error')
    return redirect(url_for('user_management'))

@app.route('/users/delete/<int:user_id>', methods=['POST', 'DELETE'])
@login_required
@role_required('owner')
def delete_user(user_id):
    """Delete a user from the database."""
    try:
        # Prevent deleting yourself
        if user_id == current_user.id:
            flash('သင့်ကိုယ်တိုင် ဖျက်လို့မရပါ။', 'error')
            return redirect(url_for('user_management'))
        
        # Check if user exists
        user = bot_db_manager.get_user_by_id(user_id)
        if not user:
            flash('User မတွေ့ပါ။', 'error')
            return redirect(url_for('user_management'))
        
        # Delete the user
        success = bot_db_manager.delete_user(user_id)
        
        if success:
            flash(f'User "{user["username"]}" ကို အောင်မြင်စွာ ဖျက်လိုက်ပါပြီ။', 'success')
        else:
            flash('User ဖျက်ရန် မအောင်မြင်ပါ။', 'error')
        
        return redirect(url_for('user_management'))
    except Exception as e:
        print(f"Error deleting user: {e}")
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('user_management'))

# ==================== BOT VERSIONING API ENDPOINTS ====================

@app.route('/api/bot/<bot_name>/versions', methods=['GET'])
@login_required
def get_bot_versions_api(bot_name):
    bot_name = unquote_plus(bot_name)
    """Get all versions of a bot"""
    try:
        versions = bot_db_manager.get_bot_versions(bot_name)
        
        # Get live and draft status
        live_version = bot_db_manager.get_bot_live_version(bot_name)
        draft_version = bot_db_manager.get_bot_draft_version(bot_name)
        
        return jsonify({
            'success': True,
            'versions': versions,
            'live_version': live_version['version_number'] if live_version else None,
            'draft_version': draft_version['version_number'] if draft_version else None
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/bot/<bot_name>/publish', methods=['POST'])
@login_required
def publish_bot_draft(bot_name):
    bot_name = unquote_plus(bot_name)
    """Publish a draft version of a bot"""
    try:
        # Decode URL-encoded bot name
        bot_name = bot_name.replace('%20', ' ')
        
        success, message = bot_db_manager.publish_draft(
            bot_name, 
            owner_id=current_user.id if current_user.is_authenticated else None
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': message
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': message
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/bot/<bot_name>/draft', methods=['GET'])
@login_required
def get_bot_draft(bot_name):
    bot_name = unquote_plus(bot_name)
    """Get the draft version of a bot"""
    try:
        # Decode URL-encoded bot name
        bot_name = bot_name.replace('%20', ' ')
        
        draft = bot_db_manager.get_bot_draft_version(bot_name)
        
        if draft:
            return jsonify({
                'success': True,
                'bot': draft
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No draft version found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/bot/<bot_name>/live', methods=['GET'])
@login_required
def get_bot_live(bot_name):
    bot_name = unquote_plus(bot_name)
    """Get the live version of a bot"""
    try:
        # Decode URL-encoded bot name
        bot_name = bot_name.replace('%20', ' ')
        
        live = bot_db_manager.get_bot_live_version(bot_name)
        
        if live:
            return jsonify({
                'success': True,
                'bot': live
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No live version found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/bot/<bot_name>/test-draft', methods=['POST'])
@login_required
def test_bot_draft(bot_name):
    bot_name = unquote_plus(bot_name)
    """Test a draft version (chat with draft without publishing)"""
    try:
        # Decode URL-encoded bot name
        bot_name = bot_name.replace('%20', ' ')
        
        data = request.get_json()
        user_message = data.get('user_message', '').strip()
        session_data = data.get('session_data', {})
        session_id = data.get('session_id') or str(uuid.uuid4())
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'user_message is required'
            }), 400
        
        # Get draft version
        bot = bot_db_manager.get_bot_draft_version(bot_name)
        if not bot:
            return jsonify({
                'success': False,
                'error': f'Draft version of bot "{bot_name}" not found'
            }), 404
        
        # Initialize Bot Logic Engine with draft
        engine = bot_logic_engine.BotLogicEngine(bot)
        
        # Process message
        start_time = datetime.now()
        result = engine.process_message(user_message, session_data)
        end_time = datetime.now()
        
        response_time = (end_time - start_time).total_seconds()
        
        bot_response = result.get('bot_response', '')
        new_session_data = result.get('session_data', {})
        intent = result.get('intent', 'unknown')
        confidence = result.get('confidence', 0.0)
        step_index = result.get('step_index')
        step_type = result.get('step_type')
        
        return jsonify({
            'success': True,
            'bot_response': bot_response,
            'session_data': new_session_data,
            'session_id': session_id,
            'intent': intent,
            'confidence': confidence,
            'step_index': step_index,
            'response_time': response_time,
            'is_draft': True
        }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Error testing draft: {str(e)}'
        }), 500

@app.route('/api/bot/<bot_name>/switch-version/<int:version_number>', methods=['POST'])
@login_required
@role_required('owner', 'editor')
def switch_bot_version(bot_name, version_number):
    """Switch to a specific version (make it live)"""
    try:
        # Decode URL-encoded bot name
        bot_name = bot_name.replace('%20', ' ')
        
        # Get all versions
        versions = bot_db_manager.get_bot_versions(bot_name)
        target_version = None
        
        for v in versions:
            if v['version_number'] == version_number:
                target_version = v
                break
        
        if not target_version:
            return jsonify({
                'success': False,
                'error': f'Version {version_number} not found'
            }), 404
        
        # Check authorization
        if current_user.role != 'owner' and target_version.get('owner_id') != current_user.id:
            return jsonify({
                'success': False,
                'error': 'Unauthorized: You don\'t have permission to switch versions'
            }), 403
        
        # Unpublish current live version
        from bot_db_manager import get_bot_db_connection
        conn = get_bot_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE bots
            SET is_live = 0
            WHERE bot_name = ? AND is_live = 1
        ''', (bot_name,))
        
        # Make target version live
        published_at = datetime.now().isoformat()
        cursor.execute('''
            UPDATE bots
            SET is_live = 1, updated_at = ?
            WHERE id = ?
        ''', (published_at, target_version['id']))
        
        # Update version history
        cursor.execute('''
            UPDATE bot_versions
            SET is_live = 1, is_draft = 0, published_at = ?
            WHERE bot_id = ? AND version_number = ?
        ''', (published_at, target_version['id'], version_number))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Switched to version {version_number}'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/templates', methods=['GET'])
@login_required
def list_templates():
    """List all available bot templates, optionally filtered by platform"""
    try:
        platform = request.args.get('platform', None)
        templates = bot_templates.list_templates(platform=platform)
        # Ensure templates is always a list
        if templates is None:
            templates = []
        return jsonify({
            'success': True,
            'templates': templates,
            'platforms': bot_templates.get_templates_by_platform()
        }), 200
    except Exception as e:
        print(f"Error loading templates: {e}")
        import traceback
        traceback.print_exc()
        # Return empty list on error instead of failing
        return jsonify({
            'success': True,
            'templates': [],
            'platforms': {}
        }), 200

@app.route('/api/templates/<template_id>', methods=['GET'])
@login_required
def get_template(template_id):
    """Get a specific bot template"""
    template = bot_templates.get_template(template_id)
    if not template:
        return jsonify({
            'success': False,
            'error': 'Template not found'
        }), 404
    
    return jsonify({
        'success': True,
        'template': template
    }), 200

@app.route('/api/templates/<template_id>/load', methods=['GET'])
@login_required
def load_template(template_id):
    """Load template data for preview/editing (doesn't create bot)"""
    try:
        template = bot_templates.get_template(template_id)
        if not template:
            return jsonify({
                'success': False,
                'error': 'Template not found'
            }), 404
        
        return jsonify({
            'success': True,
            'template': {
                'id': template_id,
                'name': template.get('name', ''),
                'description': template.get('description', ''),
                'platform': template.get('platform', 'general'),
                'initial_greeting': template.get('initial_greeting', ''),
                'steps': template.get('steps', [])
            }
        }), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Error loading template: {str(e)}'
        }), 500

@app.route('/api/templates/<template_id>/create', methods=['POST'])
@login_required
def create_from_template(template_id):
    """Create a bot from a template"""
    if not request.is_json:
        return jsonify({
            'success': False,
            'error': 'Content-Type must be application/json'
        }), 400
    
    data = request.get_json()
    bot_name = data.get('bot_name', '').strip()
    
    if not bot_name:
        return jsonify({
            'success': False,
            'error': 'Bot name is required'
        }), 400
    
    bot_config = bot_templates.create_bot_from_template(template_id, bot_name)
    if not bot_config:
        return jsonify({
            'success': False,
            'error': 'Template not found'
        }), 404
    
    # Save the bot to database (publish immediately so it shows up in lists)
    success, message, bot_id = bot_db_manager.save_bot(
        bot_name=bot_config['bot_name'],
        initial_greeting=bot_config['initial_greeting'],
        steps_data=bot_config['steps'],
        owner_id=current_user.id,
        publish=True  # Publish immediately so bot is visible
    )
    
    if success:
        return jsonify({
            'success': True,
            'message': f'Bot "{bot_config["bot_name"]}" created from template successfully',
            'bot_id': bot_id,
            'bot_name': bot_config['bot_name']
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': message
        }), 400

# ==================== GEMINI AI API ENDPOINTS ====================

@app.route('/api/gemini/chat', methods=['POST'])
@login_required
def gemini_chat():
    """
    Chat with Gemini AI
    Used for conversational advice and discussions
    """
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 400
        
        data = request.get_json()
        message = data.get('message', '').strip()
        conversation_history = data.get('conversation_history', [])
        stream = data.get('stream', False)
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        # Get Gemini service
        gemini = gemini_service.get_gemini_service()
        if not gemini:
            return jsonify({
                'success': False,
                'error': 'Gemini service is not available. Please configure GEMINI_API_KEY environment variable.'
            }), 503
        
        # Handle streaming response
        if stream:
            def generate():
                for chunk_data in gemini.chat_stream(message, conversation_history):
                    if 'error' in chunk_data:
                        yield f"data: {json.dumps({'success': False, 'error': chunk_data['error']})}\n\n"
                        break
                    yield f"data: {json.dumps({'success': True, 'chunk': chunk_data['chunk'], 'done': chunk_data['done']})}\n\n"
            
            return Response(
                generate(),
                mimetype='text/event-stream',
                headers={
                    'Cache-Control': 'no-cache',
                    'X-Accel-Buffering': 'no'
                }
            )
        
        # Handle regular response
        result = gemini.chat(message, conversation_history)
        
        if result['success']:
            return jsonify({
                'success': True,
                'response': result['response'],
                'model': result.get('model', 'gemini-pro')
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error')
            }), 500
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Error processing Gemini chat: {str(e)}'
        }), 500

@app.route('/api/gemini/status', methods=['GET'])
@login_required
def gemini_status():
    """Check if Gemini service is available"""
    try:
        is_available = gemini_service.GeminiService.is_available()
        return jsonify({
            'success': True,
            'available': is_available,
            'message': 'Gemini service is available' if is_available else 'Gemini service is not configured'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'available': False,
            'error': str(e)
        }), 500

# ==================== TELEGRAM INTEGRATION API ENDPOINTS ====================

@app.route('/api/telegram/connect/<bot_name>', methods=['POST'])
@login_required
@role_required('owner', 'editor')
def connect_telegram(bot_name):
    """Connect a bot to Telegram"""
    if not TELEGRAM_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'Telegram integration is not available. Please install python-telegram-bot: pip install python-telegram-bot'
        }), 400
    
    try:
        # Decode URL-encoded bot name
        bot_name = unquote_plus(bot_name)
        
        data = request.get_json()
        bot_token = data.get('bot_token', '').strip()
        
        if not bot_token:
            return jsonify({
                'success': False,
                'error': 'Telegram bot token is required'
            }), 400
        
        # Verify bot exists
        bot = bot_db_manager.get_bot_by_name(bot_name)
        if not bot:
            return jsonify({
                'success': False,
                'error': f'Bot "{bot_name}" not found'
            }), 404
        
        # Check if already running
        status = get_telegram_bot_status(bot_name)
        if status.get('running'):
            return jsonify({
                'success': False,
                'error': f'Telegram bot "{bot_name}" is already running'
            }), 400
        
        # Start Telegram bot in background thread
        service = start_telegram_bot(bot_name, bot_token)
        
        if service:
            return jsonify({
                'success': True,
                'message': f'Telegram bot "{bot_name}" started successfully. You can now chat with it on Telegram!'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to start Telegram bot. Please check the bot token and try again.'
            }), 500
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Error connecting to Telegram: {str(e)}'
        }), 500

@app.route('/api/telegram/disconnect/<bot_name>', methods=['POST'])
@login_required
@role_required('owner', 'editor')
def disconnect_telegram(bot_name):
    """Disconnect a bot from Telegram"""
    if not TELEGRAM_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'Telegram integration is not available'
        }), 400
    
    try:
        # Decode URL-encoded bot name
        bot_name = unquote_plus(bot_name)
        
        success = stop_telegram_bot(bot_name)
        if success:
            return jsonify({
                'success': True,
                'message': f'Telegram bot "{bot_name}" stopped successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f'Telegram bot "{bot_name}" is not running'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error disconnecting Telegram: {str(e)}'
        }), 500

@app.route('/api/telegram/status/<bot_name>', methods=['GET'])
@login_required
def telegram_status(bot_name):
    """Check Telegram bot status"""
    if not TELEGRAM_AVAILABLE:
        return jsonify({
            'success': True,
            'available': False,
            'connected': False,
            'bot_name': bot_name,
            'message': 'Telegram integration not available'
        }), 200
    
    try:
        # Decode URL-encoded bot name
        bot_name = unquote_plus(bot_name)
        
        status = get_telegram_bot_status(bot_name)
        return jsonify({
            'success': True,
            'available': True,
            'connected': status.get('running', False),
            'bot_name': bot_name
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== FACEBOOK MESSENGER INTEGRATION API ENDPOINTS ====================

@app.route('/api/facebook/connect/<bot_name>', methods=['POST'])
@login_required
@role_required('owner', 'editor')
def connect_facebook(bot_name):
    """Connect a bot to Facebook Messenger"""
    if not FACEBOOK_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'Facebook integration is not available.'
        }), 400
    
    try:
        # Decode URL-encoded bot name
        bot_name = unquote_plus(bot_name)
        
        data = request.get_json()
        page_access_token = data.get('page_access_token', '').strip()
        
        if not page_access_token:
            return jsonify({
                'success': False,
                'error': 'Facebook Page Access Token is required'
            }), 400
        
        # Verify bot exists
        bot = bot_db_manager.get_bot_by_name(bot_name)
        if not bot:
            return jsonify({
                'success': False,
                'error': f'Bot "{bot_name}" not found'
            }), 404
        
        # Check if already running
        status = get_facebook_bot_status(bot_name)
        if status.get('running'):
            return jsonify({
                'success': False,
                'error': f'Facebook bot "{bot_name}" is already running'
            }), 400
        
        # Start Facebook bot
        service = start_facebook_bot(bot_name, page_access_token)
        
        if service:
            return jsonify({
                'success': True,
                'message': f'Facebook Messenger bot "{bot_name}" started successfully. Configure webhook to receive messages.'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to start Facebook bot. Please check the Page Access Token and try again.'
            }), 500
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Error connecting to Facebook: {str(e)}'
        }), 500

@app.route('/api/facebook/disconnect/<bot_name>', methods=['POST'])
@login_required
@role_required('owner', 'editor')
def disconnect_facebook(bot_name):
    """Disconnect a bot from Facebook Messenger"""
    if not FACEBOOK_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'Facebook integration is not available'
        }), 400
    
    try:
        # Decode URL-encoded bot name
        bot_name = unquote_plus(bot_name)
        
        success = stop_facebook_bot(bot_name)
        if success:
            return jsonify({
                'success': True,
                'message': f'Facebook bot "{bot_name}" stopped successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f'Facebook bot "{bot_name}" is not running'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error disconnecting Facebook: {str(e)}'
        }), 500

@app.route('/api/facebook/status/<bot_name>', methods=['GET'])
@login_required
def facebook_status(bot_name):
    """Check Facebook Messenger bot status"""
    if not FACEBOOK_AVAILABLE:
        return jsonify({
            'success': True,
            'available': False,
            'connected': False,
            'bot_name': bot_name,
            'message': 'Facebook integration not available'
        }), 200
    
    try:
        # Decode URL-encoded bot name
        bot_name = unquote_plus(bot_name)
        
        status = get_facebook_bot_status(bot_name)
        webhook_url = get_webhook_url()
        return jsonify({
            'success': True,
            'available': True,
            'connected': status.get('running', False),
            'bot_name': bot_name,
            'webhook_url': webhook_url
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error checking Facebook status: {str(e)}'
        }), 500

@app.route('/api/facebook/webhook-url', methods=['GET'])
@login_required
def get_facebook_webhook_url():
    """Get Facebook webhook URL for configuration"""
    try:
        webhook_url = get_webhook_url()
        verify_token = os.getenv('FACEBOOK_VERIFY_TOKEN', 'azone_bot_verify_token')
        return jsonify({
            'success': True,
            'webhook_url': webhook_url,
            'verify_token': verify_token
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error getting webhook URL: {str(e)}'
        }), 500

@app.route('/webhook/facebook', methods=['GET', 'POST'])
def facebook_webhook():
    """
    Facebook Messenger webhook endpoint
    GET: Webhook verification
    POST: Receive messages
    """
    if not FACEBOOK_AVAILABLE:
        return jsonify({'error': 'Facebook integration not available'}), 400
    
    if request.method == 'GET':
        # Webhook verification
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        verify_token = os.getenv('FACEBOOK_VERIFY_TOKEN', 'azone_bot_verify_token')
        
        if mode == 'subscribe' and token == verify_token:
            logger.info("Facebook webhook verified")
            return challenge, 200
        else:
            logger.warning("Facebook webhook verification failed")
            return jsonify({'error': 'Verification failed'}), 403
    
    elif request.method == 'POST':
        # Handle incoming messages
        try:
            data = request.get_json()
            
            if data.get('object') == 'page':
                entries = data.get('entry', [])
                for entry in entries:
                    messaging = entry.get('messaging', [])
                    for event in messaging:
                        if event.get('message') and event.get('message').get('text'):
                            # Get sender ID
                            sender_id = event['sender']['id']
                            message_text = event['message']['text']
                            
                            # Find which bot should handle this (for now, use first running bot)
                            # In production, you'd map sender_id to bot_name
                            # For simplicity, we'll use the first running bot
                            if facebook_bots:
                                # Get first running bot (you can improve this logic)
                                bot_name = list(facebook_bots.keys())[0]
                                service = facebook_bots[bot_name]
                                service.process_webhook_event(event)
                            else:
                                logger.warning("No Facebook bots running to handle message")
            
            return jsonify({'status': 'ok'}), 200
            
        except Exception as e:
            logger.error(f"Error processing Facebook webhook: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid request'}), 400

if __name__ == '__main__':
    # Get host and port from config or environment (Railway sets PORT)
    try:
        import config
        # Railway provides PORT via environment variable
        port = int(os.getenv('PORT', config.Config.PORT))
        host = os.getenv('HOST', config.Config.HOST)
        debug = config.Config.DEBUG
    except:
        # Fallback if config fails
        port = int(os.getenv('PORT', 5000))
        host = os.getenv('HOST', '0.0.0.0')
        debug = False
    
    print(f"\n{'='*50}")
    print(f"🚀 Starting AZone Bot Builder Server")
    print(f"{'='*50}")
    print(f"📍 URL: http://{host}:{port}")
    print(f"🔧 Debug Mode: {debug}")
    print(f"⏰ 24/7 Mode: Enabled")
    print(f"{'='*50}\n")
    
    # Configure for 24/7 operation
    # Disable debug mode for production (prevents auto-reload)
    if debug:
        print("⚠ Warning: Debug mode enabled. For 24/7 operation, set DEBUG=False in config")
    
    try:
        # Run server with threaded=True for better handling of concurrent requests
        app.run(debug=debug, host=host, port=port, threaded=True, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n⚠ Server stopped by user (Ctrl+C)")
    except Exception as e:
        logger.error(f"Server error: {e}")
        import traceback
        traceback.print_exc()
        print(f"\n✗ Server crashed: {e}")
        print("The 24/7 keep-alive script will restart it automatically.")
        raise  # Re-raise to allow keep-alive script to detect crash