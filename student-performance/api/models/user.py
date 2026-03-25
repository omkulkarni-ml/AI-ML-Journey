"""
User and related models.
"""
from datetime import datetime
from .database import db
import bcrypt


class User(db.Model):
    """User model for authentication and profile management."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='student', nullable=False)  # student, teacher, admin
    
    # Profile info
    institution = db.Column(db.String(200), nullable=True)
    department = db.Column(db.String(100), nullable=True)
    
    # Account status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    email_verified_at = db.Column(db.DateTime, nullable=True)
    
    # Onboarding
    onboarding_completed = db.Column(db.Boolean, default=False, nullable=False)
    onboarding_step = db.Column(db.Integer, default=0, nullable=False)  # 0-3 steps
    
    # Security
    last_login_at = db.Column(db.DateTime, nullable=True)
    failed_login_attempts = db.Column(db.Integer, default=0, nullable=False)
    locked_until = db.Column(db.DateTime, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    predictions = db.relationship('PredictionHistory', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password."""
        salt = bcrypt.gensalt(rounds=12)
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        """Verify password against hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def is_locked(self):
        """Check if account is locked."""
        if self.locked_until and self.locked_until > datetime.utcnow():
            return True
        return False
    
    def to_dict(self, include_sensitive=False):
        """Convert user to dictionary."""
        data = {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': f"{self.first_name} {self.last_name}",
            'role': self.role,
            'institution': self.institution,
            'department': self.department,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'onboarding_completed': self.onboarding_completed,
            'onboarding_step': self.onboarding_step,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None
        }
        
        if include_sensitive:
            data['failed_login_attempts'] = self.failed_login_attempts
            data['locked_until'] = self.locked_until.isoformat() if self.locked_until else None
        
        return data
    
    def __repr__(self):
        return f"<User {self.email}>"


class PredictionHistory(db.Model):
    """Store user prediction history."""
    
    __tablename__ = 'prediction_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Prediction data
    input_features = db.Column(db.JSON, nullable=False)
    selected_features = db.Column(db.JSON, nullable=True)
    prediction_result = db.Column(db.JSON, nullable=False)
    prediction_grade = db.Column(db.String(2), nullable=True)  # A, B, C, D, E, F
    confidence_score = db.Column(db.Float, nullable=True)
    
    # Metadata
    model_version = db.Column(db.String(50), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert prediction history to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'input_features': self.input_features,
            'selected_features': self.selected_features,
            'prediction_result': self.prediction_result,
            'prediction_grade': self.prediction_grade,
            'confidence_score': self.confidence_score,
            'model_version': self.model_version,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f"<PredictionHistory {self.id} - User {self.user_id}>"


class RefreshToken(db.Model):
    """Store JWT refresh tokens."""
    
    __tablename__ = 'refresh_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    token = db.Column(db.String(500), unique=True, nullable=False, index=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    revoked_at = db.Column(db.DateTime, nullable=True)
    
    def is_valid(self):
        """Check if token is still valid."""
        return self.revoked_at is None and self.expires_at > datetime.utcnow()
    
    def revoke(self):
        """Revoke the token."""
        self.revoked_at = datetime.utcnow()
    
    def __repr__(self):
        return f"<RefreshToken {self.id} - User {self.user_id}>"
