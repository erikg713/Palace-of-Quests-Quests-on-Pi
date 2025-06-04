import secrets
import time
from datetime import datetime, timedelta
from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_
from app.models.user import User
from app.models.auth_tokens import RefreshToken, LoginAttempt
from app import db
from app.blueprints.auth import auth_bp
from app.blueprints.auth.forms import LoginForm, RegistrationForm, TwoFactorForm
from app.utils.security import SecurityManager, RateLimiter
from app.utils.validation import ValidationEngine
from app.utils.notifications import NotificationService

# Initialize security components
security_manager = SecurityManager()
rate_limiter = RateLimiter()
validator = ValidationEngine()
notification_service = NotificationService()

@auth_bp.route('/login', methods=['GET', 'POST'])
@rate_limiter.limit("5 per minute")
def login():
    """
    Enhanced login with comprehensive security measures including:
    - Rate limiting per IP and user
    - Suspicious activity detection
    - Device fingerprinting
    - Audit logging
    """
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    user_agent = request.headers.get('User-Agent', '')
    
    # Check for suspicious patterns
    if security_manager.is_suspicious_activity(client_ip, user_agent):
        current_app.logger.warning(f"Suspicious login attempt from {client_ip}")
        return jsonify({'error': 'Access temporarily restricted'}), 429
    
    form = LoginForm()
    
    if form.validate_on_submit():
        # Enhanced user lookup with both username and email support
        user = User.query.filter(
            or_(User.username == form.username.data.lower().strip(),
                User.email == form.username.data.lower().strip())
        ).first()
        
        # Record login attempt for analytics
        attempt = LoginAttempt(
            ip_address=client_ip,
            user_agent=user_agent,
            attempted_username=form.username.data,
            success=False,
            timestamp=datetime.utcnow()
        )
        
        if user and user.verify_password(form.password.data):
            # Check if account is locked or requires verification
            if user.is_locked:
                flash('Account temporarily locked due to security concerns. Contact support.', 'warning')
                return render_template('auth/login.html', form=form)
            
            if user.requires_email_verification and not user.email_verified:
                flash('Please verify your email before logging in.', 'info')
                return redirect(url_for('auth.resend_verification'))
            
            # Two-factor authentication check
            if user.two_factor_enabled:
                session['temp_user_id'] = user.id
                return redirect(url_for('auth.two_factor_verify'))
            
            # Successful login
            attempt.success = True
            attempt.user_id = user.id
            db.session.add(attempt)
            
            # Update user login metadata
            user.last_login = datetime.utcnow()
            user.login_count += 1
            user.last_ip_address = client_ip
            
            # Generate secure session
            login_user(user, remember=form.remember_me.data)
            
            # Create refresh token for API access
            refresh_token = RefreshToken.create_for_user(user.id)
            db.session.add(refresh_token)
            
            db.session.commit()
            
            # Log successful authentication
            current_app.logger.info(f"User {user.username} logged in from {client_ip}")
            
            # Send notification for new device login
            if security_manager.is_new_device(user.id, user_agent):
                notification_service.send_security_alert(user, 'new_device_login', {
                    'ip': client_ip,
                    'device': security_manager.parse_user_agent(user_agent),
                    'timestamp': datetime.utcnow()
                })
            
            flash('Welcome back! Login successful.', 'success')
            
            # Intelligent redirect based on user context
            next_page = request.args.get('next')
            if next_page and security_manager.is_safe_url(next_page):
                return redirect(next_page)
            
            # Context-aware dashboard redirect
            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            elif user.has_active_quests():
                return redirect(url_for('quests.active_quests'))
            else:
                return redirect(url_for('main.dashboard'))
        else:
            # Failed login handling
            db.session.add(attempt)
            db.session.commit()
            
            # Progressive delay for failed attempts
            failed_attempts = security_manager.get_recent_failed_attempts(client_ip)
            if failed_attempts > 3:
                time.sleep(min(failed_attempts * 0.5, 5))  # Max 5 second delay
            
            current_app.logger.warning(f"Failed login attempt for {form.username.data} from {client_ip}")
            flash('Invalid credentials. Please check your username and password.', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """Enhanced logout with session cleanup and audit logging."""
    user_id = current_user.id
    username = current_user.username
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    
    # Invalidate all refresh tokens for this user on this device
    RefreshToken.invalidate_for_user_device(user_id, request.headers.get('User-Agent', ''))
    
    # Clear any temporary session data
    security_manager.cleanup_user_session(user_id)
    
    logout_user()
    
    # Log logout event
    current_app.logger.info(f"User {username} logged out from {client_ip}")
    
    flash('You have been securely logged out. See you next time!', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
@rate_limiter.limit("3 per hour")
def register():
    """
    Enhanced registration with comprehensive validation and security measures.
    """
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # Advanced validation checks
        validation_result = validator.validate_registration_data({
            'username': form.username.data,
            'email': form.email.data,
            'password': form.password.data
        })
        
        if not validation_result.is_valid:
            for error in validation_result.errors:
                flash(error, 'danger')
            return render_template('auth/register.html', form=form)
        
        # Check for existing users with enhanced duplicate detection
        existing_user = User.query.filter(
            or_(User.username.ilike(form.username.data),
                User.email.ilike(form.email.data))
        ).first()
        
        if existing_user:
            if existing_user.email.lower() == form.email.data.lower():
                flash('An account with this email already exists.', 'warning')
            else:
                flash('Username already taken. Please choose a different one.', 'warning')
            return render_template('auth/register.html', form=form)
        
        try:
            # Create new user with enhanced security
            user = User(
                username=form.username.data.lower().strip(),
                email=form.email.data.lower().strip(),
                registration_ip=request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr),
                registration_date=datetime.utcnow(),
                email_verification_token=secrets.token_urlsafe(32),
                email_verification_expires=datetime.utcnow() + timedelta(hours=24)
            )
            user.set_password(form.password.data)
            
            # Initialize user profile with smart defaults
            user.initialize_profile()
            
            db.session.add(user)
            db.session.commit()
            
            # Send welcome email with verification
            notification_service.send_welcome_email(user)
            
            # Log successful registration
            current_app.logger.info(f"New user registered: {user.username} from {user.registration_ip}")
            
            flash('Registration successful! Please check your email to verify your account.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Registration error: {str(e)}")
            flash('Registration failed. Please try again later.', 'danger')
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/two-factor-verify', methods=['GET', 'POST'])
def two_factor_verify():
    """Two-factor authentication verification."""
    if 'temp_user_id' not in session:
        return redirect(url_for('auth.login'))
    
    form = TwoFactorForm()
    user = User.query.get(session['temp_user_id'])
    
    if form.validate_on_submit():
        if user.verify_totp(form.token.data):
            # Complete login process
            session.pop('temp_user_id', None)
            login_user(user)
            
            flash('Two-factor authentication successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid authentication code. Please try again.', 'danger')
    
    return render_template('auth/two_factor.html', form=form)

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
@rate_limiter.limit("3 per hour")
def forgot_password():
    """Enhanced password reset with security measures."""
    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        
        if not validator.is_valid_email(email):
            flash('Please enter a valid email address.', 'danger')
            return render_template('auth/forgot_password.html')
        
        user = User.query.filter_by(email=email).first()
        
        # Always show success message to prevent email enumeration
        flash('If an account with this email exists, you will receive password reset instructions.', 'info')
        
        if user:
            # Generate secure reset token
            reset_token = user.generate_password_reset_token()
            notification_service.send_password_reset_email(user, reset_token)
            
            current_app.logger.info(f"Password reset requested for {email}")
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html')

@auth_bp.route('/verify-email/<token>')
def verify_email(token):
    """Email verification handler with enhanced security."""
    user = User.verify_email_token(token)
    
    if user:
        user.email_verified = True
        user.email_verification_token = None
        user.email_verification_expires = None
        db.session.commit()
        
        current_app.logger.info(f"Email verified for user: {user.username}")
        flash('Email verified successfully! You can now log in.', 'success')
    else:
        flash('Invalid or expired verification link.', 'danger')
    
    return redirect(url_for('auth.login'))
