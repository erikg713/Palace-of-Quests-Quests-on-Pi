"""
Authentication routes with enhanced security and user experience.
Implements rate limiting, session management, and comprehensive validation.

Author: Erik G. - Palace of Quests Team
Last Updated: 2025-06-04
"""

import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Optional, Dict, Any

from flask import render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.models.audit_log import AuditLog
from app import db
from app.blueprints.auth import auth_bp
from app.blueprints.auth.forms import LoginForm, RegistrationForm, PasswordResetForm
from app.utils.rate_limiter import rate_limit
from app.utils.validators import validate_password_strength, validate_email_format
from app.utils.security import generate_csrf_token, verify_csrf_token

logger = logging.getLogger(__name__)

# Constants for security policies
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = timedelta(minutes=30)
SESSION_TIMEOUT = timedelta(hours=24)

def log_security_event(event_type: str, user_id: Optional[int] = None, 
                      details: Optional[Dict] = None):
    """Log security-related events for audit purposes."""
    try:
        audit_entry = AuditLog(
            event_type=event_type,
            user_id=user_id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', ''),
            details=details or {},
            timestamp=datetime.utcnow()
        )
        db.session.add(audit_entry)
        db.session.commit()
    except Exception as e:
        logger.error(f"Failed to log security event: {str(e)}")

def check_account_lockout(username: str) -> bool:
    """Check if account is currently locked due to failed attempts."""
    recent_attempts = AuditLog.query.filter(
        AuditLog.event_type == 'failed_login',
        AuditLog.details.contains({'username': username}),
        AuditLog.timestamp > datetime.utcnow() - LOCKOUT_DURATION
    ).count()
    
    return recent_attempts >= MAX_LOGIN_ATTEMPTS

@auth_bp.route('/login', methods=['GET', 'POST'])
@rate_limit(max_requests=10, window=300)  # 10 requests per 5 minutes
def login():
    """Enhanced login with security features and better UX."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    
    if request.method == 'POST':
        if not verify_csrf_token(request.form.get('csrf_token')):
            flash('Security token validation failed. Please try again.', 'error')
            return render_template('auth/login.html', form=form)
        
        if form.validate_on_submit():
            username = form.username.data.strip().lower()
            
            # Check for account lockout
            if check_account_lockout(username):
                log_security_event('blocked_login_attempt', details={'username': username})
                flash(
                    'Account temporarily locked due to multiple failed attempts. '
                    'Please try again in 30 minutes.',
                    'warning'
                )
                return render_template('auth/login.html', form=form)
            
            user = User.query.filter_by(username=username).first()
            
            if user and user.is_active and user.check_password(form.password.data):
                # Successful login
                login_user(user, remember=form.remember_me.data, 
                          duration=SESSION_TIMEOUT)
                
                # Update user's last login
                user.last_login = datetime.utcnow()
                user.login_count += 1
                db.session.commit()
                
                log_security_event('successful_login', user_id=user.id)
                
                # Handle next URL with security validation
                next_page = request.args.get('next')
                if next_page and next_page.startswith('/'):
                    flash(f'Welcome back, {user.display_name}!', 'success')
                    return redirect(next_page)
                
                flash(f'Welcome back, {user.display_name}!', 'success')
                return redirect(url_for('main.dashboard'))
            else:
                # Failed login attempt
                log_security_event(
                    'failed_login',
                    user_id=user.id if user else None,
                    details={'username': username, 'reason': 'invalid_credentials'}
                )
                flash('Invalid username or password. Please check your credentials.', 'error')
        else:
            # Form validation failed
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{field.title()}: {error}', 'error')
    
    # Generate CSRF token for form
    csrf_token = generate_csrf_token()
    return render_template('auth/login.html', form=form, csrf_token=csrf_token)

@auth_bp.route('/logout')
@login_required
def logout():
    """Secure logout with session cleanup."""
    user_id = current_user.id
    username = current_user.username
    
    # Log the logout event
    log_security_event('user_logout', user_id=user_id)
    
    # Clear user session data
    session.clear()
    logout_user()
    
    flash(f'You have been securely logged out, {username}. See you next time!', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
@rate_limit(max_requests=5, window=3600)  # 5 registrations per hour
def register():
    """Enhanced user registration with validation and security."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    
    if request.method == 'POST':
        if not verify_csrf_token(request.form.get('csrf_token')):
            flash('Security token validation failed. Please try again.', 'error')
            return render_template('auth/register.html', form=form)
        
        if form.validate_on_submit():
            username = form.username.data.strip().lower()
            email = form.email.data.strip().lower()
            
            # Enhanced validation
            if not validate_email_format(email):
                flash('Please provide a valid email address.', 'error')
                return render_template('auth/register.html', form=form)
            
            password_validation = validate_password_strength(form.password.data)
            if not password_validation['valid']:
                for error in password_validation['errors']:
                    flash(error, 'error')
                return render_template('auth/register.html', form=form)
            
            # Check for existing users
            existing_user = User.query.filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing_user:
                if existing_user.username == username:
                    flash('Username already taken. Please choose a different one.', 'error')
                else:
                    flash('Email already registered. Please use a different email or try logging in.', 'error')
                return render_template('auth/register.html', form=form)
            
            try:
                # Create new user
                user = User(
                    username=username,
                    email=email,
                    display_name=form.display_name.data.strip() or username.title(),
                    created_at=datetime.utcnow(),
                    is_active=True,
                    email_verified=False  # Will be verified later
                )
                user.set_password(form.password.data)
                
                db.session.add(user)
                db.session.commit()
                
                log_security_event('user_registration', user_id=user.id)
                
                flash(
                    'Registration successful! Welcome to Palace of Quests. '
                    'Please check your email to verify your account.',
                    'success'
                )
                
                # Auto-login after registration
                login_user(user)
                return redirect(url_for('main.welcome'))
                
            except IntegrityError as e:
                db.session.rollback()
                logger.error(f"Registration failed for {username}: {str(e)}")
                flash('Registration failed due to a database error. Please try again.', 'error')
            except Exception as e:
                db.session.rollback()
                logger.error(f"Unexpected registration error: {str(e)}")
                flash('An unexpected error occurred. Please try again later.', 'error')
        else:
            # Form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{field.replace("_", " ").title()}: {error}', 'error')
    
    csrf_token = generate_csrf_token()
    return render_template('auth/register.html', form=form, csrf_token=csrf_token)

@auth_bp.route('/profile/settings')
@login_required
def profile_settings():
    """User profile management with enhanced security."""
    return render_template('auth/profile_settings.html', user=current_user)

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
@rate_limit(max_requests=3, window=3600)  # 3 requests per hour
def forgot_password():
    """Password reset functionality with security measures."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = PasswordResetForm()
    
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Generate password reset token (implement token generation)
            log_security_event('password_reset_requested', user_id=user.id)
            # Send password reset email (implement email sending)
        
        # Always show success message for security
        flash(
            'If an account with that email exists, '
            'password reset instructions have been sent.',
            'info'
        )
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html', form=form)

@auth_bp.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limiting errors."""
    return jsonify({
        'error': 'Too many requests',
        'message': 'Please wait before trying again.',
        'retry_after': e.retry_after
    }), 429
