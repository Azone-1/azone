"""
Session Middleware
Handles session timeout, validation, and cleanup
"""

from flask import session, request, redirect, url_for, jsonify
from functools import wraps
from datetime import datetime
import auth_manager

def check_session_timeout():
    """Check if current session has expired"""
    session_token = session.get('session_token')
    expires_at = session.get('expires_at')
    
    if not session_token or not expires_at:
        return False
    
    try:
        expires_dt = datetime.fromisoformat(expires_at)
        if datetime.now() >= expires_dt:
            return False
    except:
        return False
    
    # Validate session in database
    session_data = auth_manager.validate_session(session_token)
    if not session_data:
        return False
    
    return True

def session_timeout_required(f):
    """Decorator to check session timeout before route execution"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not check_session_timeout():
            # Session expired
            session.clear()
            
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({
                    'success': False,
                    'error': 'Session expired. Please login again.',
                    'session_expired': True
                }), 401
            
            from flask_login import logout_user
            logout_user()
            return redirect(url_for('auth.login', next=request.path))
        
        return f(*args, **kwargs)
    return decorated_function

def cleanup_expired_sessions_periodically():
    """Clean up expired sessions (call this periodically)"""
    auth_manager.cleanup_expired_sessions()

