"""
Authentication API routes.
"""
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from models import db, User, RefreshToken
from utils.validators import (
    validate_email, validate_password, validate_name,
    validate_institution, validate_department, validate_role
)
from utils.security import generate_secure_token
from utils.logger import get_logger

auth_bp = Blueprint('auth', __name__)
logger = get_logger('auth')

# Token blacklist for logout
blacklist = set()


@auth_bp.route('/auth/register', methods=['POST'])
def register():
    """
    Register a new user.
    
    Request body:
        {
            "email": "user@example.com",
            "password": "SecurePass123!",
            "first_name": "John",
            "last_name": "Doe",
            "role": "student" (optional),
            "institution": "University" (optional),
            "department": "CS" (optional)
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate email
        email_valid, email, email_error = validate_email(data.get('email'))
        if not email_valid:
            return jsonify({
                'success': False,
                'error': email_error
            }), 400
        
        # Validate password
        password_valid, password_error = validate_password(data.get('password'))
        if not password_valid:
            return jsonify({
                'success': False,
                'error': password_error
            }), 400
        
        # Validate names
        first_name_valid, first_name, fn_error = validate_name(
            data.get('first_name'), 'First name'
        )
        if not first_name_valid:
            return jsonify({
                'success': False,
                'error': fn_error
            }), 400
        
        last_name_valid, last_name, ln_error = validate_name(
            data.get('last_name'), 'Last name'
        )
        if not last_name_valid:
            return jsonify({
                'success': False,
                'error': ln_error
            }), 400
        
        # Validate optional fields
        role_valid, role, role_error = validate_role(data.get('role'))
        if not role_valid:
            return jsonify({
                'success': False,
                'error': role_error
            }), 400
        
        inst_valid, institution, inst_error = validate_institution(
            data.get('institution')
        )
        if not inst_valid:
            return jsonify({
                'success': False,
                'error': inst_error
            }), 400
        
        dept_valid, department, dept_error = validate_department(
            data.get('department')
        )
        if not dept_valid:
            return jsonify({
                'success': False,
                'error': dept_error
            }), 400
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            return jsonify({
                'success': False,
                'error': 'Email already registered'
            }), 409
        
        # Create new user
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            institution=institution,
            department=department
        )
        user.set_password(data.get('password'))
        
        db.session.add(user)
        db.session.commit()
        
        logger.info(f"New user registered: {email}")
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'data': {
                'user': user.to_dict()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Registration error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Registration failed. Please try again.'
        }), 500


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """
    Authenticate user and return tokens.
    
    Request body:
        {
            "email": "user@example.com",
            "password": "password"
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'error': 'Email and password are required'
            }), 400
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and is active
        if not user:
            logger.warning(f"Login attempt for non-existent user: {email}")
            return jsonify({
                'success': False,
                'error': 'Invalid credentials'
            }), 401
        
        # Check if account is locked
        if user.is_locked():
            logger.warning(f"Login attempt for locked account: {email}")
            return jsonify({
                'success': False,
                'error': 'Account is temporarily locked. Please try again later.'
            }), 403
        
        if not user.is_active:
            logger.warning(f"Login attempt for deactivated account: {email}")
            return jsonify({
                'success': False,
                'error': 'Account is deactivated'
            }), 403
        
        # Verify password
        if not user.check_password(password):
            # Increment failed login attempts
            user.failed_login_attempts += 1
            
            # Lock account after 5 failed attempts
            if user.failed_login_attempts >= 5:
                user.locked_until = datetime.utcnow() + timedelta(minutes=30)
                logger.warning(f"Account locked due to failed attempts: {email}")
            
            db.session.commit()
            
            return jsonify({
                'success': False,
                'error': 'Invalid credentials'
            }), 401
        
        # Reset failed login attempts on successful login
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login_at = datetime.utcnow()
        db.session.commit()
        
        # Generate tokens
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(hours=1)
        )
        refresh_token = create_refresh_token(
            identity=user.id,
            expires_delta=timedelta(days=30)
        )
        
        # Store refresh token
        token_record = RefreshToken(
            user_id=user.id,
            token=refresh_token,
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        db.session.add(token_record)
        db.session.commit()
        
        logger.info(f"User logged in: {email}")
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'data': {
                'user': user.to_dict(),
                'tokens': {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'token_type': 'Bearer',
                    'expires_in': 3600  # 1 hour
                }
            }
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Login error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Login failed. Please try again.'
        }), 500


@auth_bp.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token using refresh token."""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.is_active:
            return jsonify({
                'success': False,
                'error': 'User not found or inactive'
            }), 401
        
        # Create new access token
        access_token = create_access_token(
            identity=user_id,
            expires_delta=timedelta(hours=1)
        )
        
        return jsonify({
            'success': True,
            'data': {
                'access_token': access_token,
                'token_type': 'Bearer',
                'expires_in': 3600
            }
        })
        
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Token refresh failed'
        }), 500


@auth_bp.route('/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user and revoke token."""
    try:
        jti = get_jwt()['jti']
        blacklist.add(jti)
        
        user_id = get_jwt_identity()
        logger.info(f"User logged out: {user_id}")
        
        return jsonify({
            'success': True,
            'message': 'Logout successful'
        })
        
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Logout failed'
        }), 500


@auth_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user info."""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict()
            }
        })
        
    except Exception as e:
        logger.error(f"Get user error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get user info'
        }), 500


@auth_bp.route('/auth/onboarding', methods=['PUT'])
@jwt_required()
def update_onboarding():
    """
    Update user onboarding status.
    
    Request body:
        {
            "step": 1,
            "completed": false,
            "institution": "University",
            "department": "CS"
        }
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        data = request.get_json()
        
        # Update onboarding step
        if 'step' in data:
            step = data['step']
            if not isinstance(step, int) or step < 0 or step > 3:
                return jsonify({
                    'success': False,
                    'error': 'Invalid onboarding step'
                }), 400
            user.onboarding_step = step
        
        # Update completion status
        if 'completed' in data:
            user.onboarding_completed = bool(data['completed'])
        
        # Update profile info
        if 'institution' in data:
            inst_valid, institution, inst_error = validate_institution(data['institution'])
            if not inst_valid:
                return jsonify({
                    'success': False,
                    'error': inst_error
                }), 400
            user.institution = institution
        
        if 'department' in data:
            dept_valid, department, dept_error = validate_department(data['department'])
            if not dept_valid:
                return jsonify({
                    'success': False,
                    'error': dept_error
                }), 400
            user.department = department
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Onboarding updated',
            'data': {
                'user': user.to_dict()
            }
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Onboarding update error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to update onboarding'
        }), 500


@auth_bp.route('/auth/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    """
    Change user password.
    
    Request body:
        {
            "current_password": "oldpass",
            "new_password": "newpass"
        }
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({
                'success': False,
                'error': 'Current and new passwords are required'
            }), 400
        
        # Verify current password
        if not user.check_password(current_password):
            return jsonify({
                'success': False,
                'error': 'Current password is incorrect'
            }), 401
        
        # Validate new password
        password_valid, password_error = validate_password(new_password)
        if not password_valid:
            return jsonify({
                'success': False,
                'error': password_error
            }), 400
        
        # Set new password
        user.set_password(new_password)
        db.session.commit()
        
        logger.info(f"Password changed for user: {user.email}")
        
        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Password change error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to change password'
        }), 500
