"""
Input validation utilities.
"""
import re
import bleach
from email_validator import validate_email as email_validator, EmailNotValidError


def validate_email(email):
    """
    Validate email address format.
    
    Args:
        email: Email string to validate
        
    Returns:
        tuple: (is_valid: bool, normalized_email: str or None, error_message: str or None)
    """
    if not email or not isinstance(email, str):
        return False, None, "Email is required"
    
    email = email.strip().lower()
    
    try:
        validation = email_validator(email, check_deliverability=False)
        return True, validation.email, None
    except EmailNotValidError as e:
        return False, None, str(e)


def validate_password(password):
    """
    Validate password strength.
    
    Requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    
    Args:
        password: Password string to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-=+\[\]\\;/`~]', password):
        return False, "Password must contain at least one special character"
    
    return True, None


def validate_name(name, field_name="Name"):
    """
    Validate name field.
    
    Args:
        name: Name string to validate
        field_name: Field name for error messages
        
    Returns:
        tuple: (is_valid: bool, sanitized_name: str or None, error_message: str or None)
    """
    if not name or not isinstance(name, str):
        return False, None, f"{field_name} is required"
    
    name = name.strip()
    
    if len(name) < 1:
        return False, None, f"{field_name} is required"
    
    if len(name) > 100:
        return False, None, f"{field_name} must be less than 100 characters"
    
    # Allow letters, spaces, hyphens, and apostrophes
    if not re.match(r"^[a-zA-Z\s'-]+$", name):
        return False, None, f"{field_name} contains invalid characters"
    
    return True, name, None


def sanitize_input(text, allowed_tags=None):
    """
    Sanitize user input to prevent XSS attacks.
    
    Args:
        text: Text to sanitize
        allowed_tags: List of allowed HTML tags (default: none)
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    if allowed_tags is None:
        allowed_tags = []
    
    allowed_attributes = {}
    
    return bleach.clean(str(text), tags=allowed_tags, attributes=allowed_attributes, strip=True)


def validate_institution(institution):
    """
    Validate institution name.
    
    Args:
        institution: Institution string to validate
        
    Returns:
        tuple: (is_valid: bool, sanitized: str or None, error_message: str or None)
    """
    if not institution:
        return True, None, None  # Optional field
    
    if not isinstance(institution, str):
        return False, None, "Institution must be a string"
    
    institution = institution.strip()
    
    if len(institution) > 200:
        return False, None, "Institution name must be less than 200 characters"
    
    sanitized = sanitize_input(institution)
    return True, sanitized, None


def validate_department(department):
    """
    Validate department name.
    
    Args:
        department: Department string to validate
        
    Returns:
        tuple: (is_valid: bool, sanitized: str or None, error_message: str or None)
    """
    if not department:
        return True, None, None  # Optional field
    
    if not isinstance(department, str):
        return False, None, "Department must be a string"
    
    department = department.strip()
    
    if len(department) > 100:
        return False, None, "Department name must be less than 100 characters"
    
    sanitized = sanitize_input(department)
    return True, sanitized, None


def validate_role(role):
    """
    Validate user role.
    
    Args:
        role: Role string to validate
        
    Returns:
        tuple: (is_valid: bool, normalized_role: str or None, error_message: str or None)
    """
    valid_roles = ['student', 'teacher', 'admin']
    
    if not role:
        return True, 'student', None  # Default to student
    
    role = role.strip().lower()
    
    if role not in valid_roles:
        return False, None, f"Invalid role. Must be one of: {', '.join(valid_roles)}"
    
    return True, role, None
