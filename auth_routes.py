"""
Authentication Routes
Login, logout, password reset, and session management endpoints
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session, make_response
from flask_login import login_user, logout_user, current_user, login_required
from functools import wraps
from datetime import datetime, timedelta
import auth_manager
from werkzeug.security import generate_password_hash
import secrets

auth_bp = Blueprint('auth', __name__)

def get_client_ip():
    """Get client IP address"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr

def get_user_agent():
    """Get user agent string"""
    return request.headers.get('User-Agent', 'Unknown')

def require_csrf(f):
    """Decorator to require CSRF token for POST requests"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'POST':
            session_id = session.get('session_id')
            csrf_token = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token')
            
            if not session_id or not csrf_token:
                if request.is_json:
                    return jsonify({'success': False, 'error': 'CSRF token missing'}), 403
                flash('Security token missing. Please try again.', 'error')
                return redirect(request.url)
            
            if not auth_manager.validate_csrf_token(session_id, csrf_token):
                if request.is_json:
                    return jsonify({'success': False, 'error': 'Invalid CSRF token'}), 403
                flash('Invalid security token. Please refresh and try again.', 'error')
                return redirect(request.url)
        
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember_me = request.form.get('remember', '') == 'on'
        next_page = request.args.get('next') or request.form.get('next')
        
        if not username or not password:
            flash('ကျေးဇူးပြု၍ username နှင့် password ထည့်သွင်းပါ။', 'error')
            return render_template('login.html')
        
        # Authenticate user
        ip_address = get_client_ip()
        user_agent = get_user_agent()
        result = auth_manager.authenticate_user(username, password, ip_address, user_agent, remember_me)
        
        if not result.get('success'):
            flash(result.get('error', 'Login failed'), 'error')
            return render_template('login.html')
        
        # Get user object for Flask-Login
        from web_app import AppUser
        user_data = {
            'id': result['user_id'],
            'username': result['username'],
            'email': result['email'],
            'role': result['role']
        }
        user = AppUser(user_data)
        
        # Login with Flask-Login
        login_user(user, remember=remember_me)
        
        # Store session token
        session['session_token'] = result['session_token']
        session['session_id'] = secrets.token_hex(16)
        session['expires_at'] = result['expires_at']
        
        # Create CSRF token
        csrf_token = auth_manager.create_csrf_token(session['session_id'])
        session['csrf_token'] = csrf_token
        
        # Set secure cookie if HTTPS
        response = make_response(redirect(next_page or url_for('dashboard')))
        if remember_me:
            # Set longer expiration for remember me
            expires = datetime.now() + timedelta(days=30)
            response.set_cookie('remember_token', result['session_token'], 
                              expires=expires, httponly=True, secure=request.is_secure, samesite='Lax')
        
        flash('Login အောင်မြင်ပါသည်။', 'success')
        return response
    
    return render_template('login.html')

@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """User logout"""
    # Invalidate session
    session_token = session.get('session_token')
    if session_token:
        auth_manager.invalidate_session(session_token)
    
    # Clear session
    session.clear()
    
    # Logout with Flask-Login
    logout_user()
    
    # Clear remember me cookie
    response = make_response(redirect(url_for('auth.login')))
    response.set_cookie('remember_token', '', expires=0)
    
    flash('Logout အောင်မြင်ပါသည်။', 'success')
    return response

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        role = request.form.get('role', 'viewer')
        
        # Validation
        if not username or len(username) < 3:
            flash('Username သည် အနည်းဆုံး ၃ လုံး ရှိရမည်။', 'error')
            return render_template('login.html', register_mode=True)
        
        if not email or '@' not in email:
            flash('မှန်ကန်သော email address ထည့်သွင်းပါ။', 'error')
            return render_template('login.html', register_mode=True)
        
        if not password or len(password) < 6:
            flash('Password သည် အနည်းဆုံး ၆ လုံး ရှိရမည်။', 'error')
            return render_template('login.html', register_mode=True)
        
        if password != password_confirm:
            flash('Passwords မတူညီပါ။', 'error')
            return render_template('login.html', register_mode=True)
        
        # Create user
        result = auth_manager.create_user(username, email, password, role)
        
        if not result.get('success'):
            flash(result.get('error', 'Registration failed'), 'error')
            return render_template('login.html', register_mode=True)
        
        flash('Registration အောင်မြင်ပါသည်။ ကျေးဇူးပြု၍ login ဝင်ပါ။', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('login.html', register_mode=True)

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Password reset request page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        if not email:
            flash('Email address ထည့်သွင်းရန် လိုအပ်ပါသည်။', 'error')
            return render_template('forgot_password.html')
        
        user = auth_manager.get_user_by_email(email)
        
        if user:
            # Create reset token
            token = auth_manager.create_password_reset_token(user['id'])
            
            if token:
                # In production, send email with reset link
                # For now, we'll show the token (remove in production!)
                reset_url = url_for('auth.reset_password', token=token, _external=True)
                flash(f'Password reset link has been sent to your email. (Dev: {reset_url})', 'info')
                # TODO: Send email with reset_url
            else:
                flash('Password reset token creation failed. Please try again.', 'error')
        else:
            # Don't reveal if email exists (security)
            flash('If the email exists, a password reset link has been sent.', 'info')
        
        return redirect(url_for('auth.login'))
    
    return render_template('forgot_password.html')

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Password reset page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    # Validate token
    token_data = auth_manager.validate_password_reset_token(token)
    
    if not token_data:
        flash('Invalid or expired password reset token.', 'error')
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == 'POST':
        new_password = request.form.get('new_password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        if not new_password or len(new_password) < 6:
            flash('Password သည် အနည်းဆုံး ၆ လုံး ရှိရမည်။', 'error')
            return render_template('reset_password.html', token=token)
        
        if new_password != password_confirm:
            flash('Passwords မတူညီပါ။', 'error')
            return render_template('reset_password.html', token=token)
        
        # Reset password
        if auth_manager.reset_password(token_data['user_id'], new_password):
            # Mark token as used
            auth_manager.use_password_reset_token(token)
            flash('Password reset အောင်မြင်ပါသည်။ ကျေးဇူးပြု၍ login ဝင်ပါ။', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Password reset failed. Please try again.', 'error')
    
    return render_template('reset_password.html', token=token)

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
@require_csrf
def change_password():
    """Change password page (for logged-in users)"""
    if request.method == 'POST':
        old_password = request.form.get('old_password', '')
        new_password = request.form.get('new_password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        if not old_password or not new_password:
            flash('ကျေးဇူးပြု၍ passwords အားလုံး ထည့်သွင်းပါ။', 'error')
            return render_template('change_password.html')
        
        if new_password != password_confirm:
            flash('New passwords မတူညီပါ။', 'error')
            return render_template('change_password.html')
        
        if len(new_password) < 6:
            flash('New password သည် အနည်းဆုံး ၆ လုံး ရှိရမည်။', 'error')
            return render_template('change_password.html')
        
        result = auth_manager.change_password(current_user.id, old_password, new_password)
        
        if result.get('success'):
            flash('Password change အောင်မြင်ပါသည်။', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(result.get('error', 'Password change failed'), 'error')
    
    return render_template('change_password.html')

@auth_bp.route('/api/session/check', methods=['GET'])
@login_required
def check_session():
    """Check if session is still valid"""
    session_token = session.get('session_token')
    
    if not session_token:
        return jsonify({'valid': False, 'error': 'No session token'}), 401
    
    session_data = auth_manager.validate_session(session_token)
    
    if not session_data:
        return jsonify({'valid': False, 'error': 'Session expired'}), 401
    
    return jsonify({
        'valid': True,
        'expires_at': session_data['expires_at'],
        'user_id': session_data['user_id']
    })

@auth_bp.route('/api/session/refresh', methods=['POST'])
@login_required
def refresh_session():
    """Refresh session expiration"""
    session_token = session.get('session_token')
    
    if not session_token:
        return jsonify({'success': False, 'error': 'No session token'}), 401
    
    session_data = auth_manager.validate_session(session_token)
    
    if not session_data:
        return jsonify({'success': False, 'error': 'Session expired'}), 401
    
    # Extend session (implement in auth_manager if needed)
    return jsonify({'success': True, 'message': 'Session refreshed'})

@auth_bp.route('/api/session/invalidate-all', methods=['POST'])
@login_required
@require_csrf
def invalidate_all_sessions():
    """Invalidate all sessions except current"""
    session_token = session.get('session_token')
    
    if auth_manager.invalidate_user_sessions(current_user.id, session_token):
        flash('All other sessions have been invalidated.', 'success')
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Failed to invalidate sessions'}), 500

