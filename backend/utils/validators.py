"""
Comprehensive Request Validators
Enhanced validation with detailed error messages and security checks
"""

from functools import wraps
from flask import request, jsonify
import logging
import structlog
from typing import List, Dict, Any, Callable
import re
from datetime import datetime

logger = structlog.get_logger()

def validate_request_data(required_fields: List[str], optional_fields: List[str] = None):
    """
    Decorator to validate request data
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Check if request has JSON data
                if not request.is_json:
                    return jsonify({
                        'error': 'Invalid Content-Type',
                        'message': 'Request must contain JSON data',
                        'status_code': 400
                    }), 400
                
                data = request.get_json()
                if not data:
                    return jsonify({
                        'error': 'Empty Request',
                        'message': 'Request body cannot be empty',
                        'status_code': 400
                    }), 400
                
                # Check required fields
                missing_fields = []
                for field in required_fields:
                    if field not in data or data[field] is None or data[field] == '':
                        missing_fields.append(field)
                
                if missing_fields:
                    return jsonify({
                        'error': 'Missing Required Fields',
                        'message': f'The following fields are required: {", ".join(missing_fields)}',
                        'missing_fields': missing_fields,
                        'status_code': 400
                    }), 400
                
                # Validate field formats
                validation_errors = validate_field_formats(data, required_fields + (optional_fields or []))
                if validation_errors:
                    return jsonify({
                        'error': 'Validation Error',
                        'message': 'One or more fields have invalid formats',
                        'validation_errors': validation_errors,
                        'status_code': 400
                    }), 400
                
                # Security validation
                security_errors = validate_security(data)
                if security_errors:
                    logger.warning("Security validation failed", errors=security_errors)
                    return jsonify({
                        'error': 'Security Validation Failed',
                        'message': 'Request contains potentially harmful content',
                        'status_code': 400
                    }), 400
                
                return f(*args, **kwargs)
                
            except Exception as e:
                logger.error("Request validation error", error=str(e))
                return jsonify({
                    'error': 'Validation Error',
                    'message': 'Request validation failed',
                    'status_code': 500
                }), 500
        
        return decorated_function
    return decorator

def validate_field_formats(data: Dict[str, Any], fields: List[str]) -> List[Dict[str, str]]:
    """
    Validate field formats
    """
    errors = []
    
    for field in fields:
        if field in data and data[field] is not None:
            value = data[field]
            
            # Email validation
            if 'email' in field.lower() and isinstance(value, str):
                if not is_valid_email(value):
                    errors.append({
                        'field': field,
                        'message': 'Invalid email format'
                    })
            
            # Password validation
            elif 'password' in field.lower() and isinstance(value, str):
                password_errors = validate_password_strength(value)
                if password_errors:
                    errors.extend([{
                        'field': field,
                        'message': error
                    } for error in password_errors])
            
            # URL validation
            elif 'url' in field.lower() and isinstance(value, str):
                if not is_valid_url(value):
                    errors.append({
                        'field': field,
                        'message': 'Invalid URL format'
                    })
            
            # Date validation
            elif 'date' in field.lower() and isinstance(value, str):
                if not is_valid_date(value):
                    errors.append({
                        'field': field,
                        'message': 'Invalid date format (expected ISO 8601)'
                    })
            
            # Numeric validation
            elif field.endswith('_id') or 'count' in field.lower():
                if not isinstance(value, (int, float)) or value < 0:
                    errors.append({
                        'field': field,
                        'message': 'Must be a non-negative number'
                    })
    
    return errors

def validate_security(data: Dict[str, Any]) -> List[str]:
    """
    Validate request for security issues
    """
    errors = []
    
    # Check for SQL injection patterns
    sql_injection_patterns = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)",
        r"(--|#|/\*|\*/)",
        r"(\b(OR|AND)\s+\d+\s*=\s*\d+)",
        r"(\b(OR|AND)\s+['\"].*['\"])"
    ]
    
    # Check for XSS patterns
    xss_patterns = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",
        r"<iframe[^>]*>.*?</iframe>"
    ]
    
    # Check for path traversal
    path_traversal_patterns = [
        r"\.\./",
        r"\.\.\\",
        r"%2e%2e%2f",
        r"%2e%2e%5c"
    ]
    
    def check_patterns(value: str, patterns: List[str], error_type: str):
        for pattern in patterns:
            if re.search(pattern, value, re.IGNORECASE):
                errors.append(f"Potential {error_type} detected")
                break
    
    # Recursively check all string values
    def check_value(value, key=""):
        if isinstance(value, str):
            check_patterns(value, sql_injection_patterns, "SQL injection")
            check_patterns(value, xss_patterns, "XSS attack")
            check_patterns(value, path_traversal_patterns, "path traversal")
            
            # Check for excessively long strings
            if len(value) > 10000:
                errors.append(f"Field '{key}' exceeds maximum length")
        
        elif isinstance(value, dict):
            for k, v in value.items():
                check_value(v, k)
        
        elif isinstance(value, list):
            for i, item in enumerate(value):
                check_value(item, f"{key}[{i}]")
    
    check_value(data)
    return errors

def is_valid_email(email: str) -> bool:
    """
    Validate email format
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password_strength(password: str) -> List[str]:
    """
    Validate password strength
    """
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one digit")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character")
    
    # Check for common weak passwords
    weak_passwords = [
        'password', '123456', 'password123', 'admin', 'qwerty',
        'letmein', 'welcome', 'monkey', '1234567890'
    ]
    
    if password.lower() in weak_passwords:
        errors.append("Password is too common and easily guessable")
    
    return errors

def is_valid_url(url: str) -> bool:
    """
    Validate URL format
    """
    pattern = r'^https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$'
    return re.match(pattern, url) is not None

def is_valid_date(date_string: str) -> bool:
    """
    Validate ISO 8601 date format
    """
    try:
        datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False

def validate_file_upload(file, allowed_extensions: List[str], max_size_mb: int = 100) -> List[str]:
    """
    Validate file upload
    """
    errors = []
    
    if not file:
        errors.append("No file provided")
        return errors
    
    if not file.filename:
        errors.append("No filename provided")
        return errors
    
    # Check file extension
    if '.' not in file.filename:
        errors.append("File must have an extension")
    else:
        extension = file.filename.rsplit('.', 1)[1].lower()
        if extension not in allowed_extensions:
            errors.append(f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}")
    
    # Check file size
    file.seek(0, 2)  # Seek to end of file
    file_size = file.tell()
    file.seek(0)  # Reset file pointer
    
    max_size_bytes = max_size_mb * 1024 * 1024
    if file_size > max_size_bytes:
        errors.append(f"File size exceeds maximum allowed size of {max_size_mb}MB")
    
    if file_size == 0:
        errors.append("File is empty")
    
    return errors

def validate_coordinates(latitude: float, longitude: float) -> List[str]:
    """
    Validate geographic coordinates
    """
    errors = []
    
    if not isinstance(latitude, (int, float)):
        errors.append("Latitude must be a number")
    elif latitude < -90 or latitude > 90:
        errors.append("Latitude must be between -90 and 90 degrees")
    
    if not isinstance(longitude, (int, float)):
        errors.append("Longitude must be a number")
    elif longitude < -180 or longitude > 180:
        errors.append("Longitude must be between -180 and 180 degrees")
    
    return errors

def validate_carbon_data(data: Dict[str, Any]) -> List[str]:
    """
    Validate carbon footprint data
    """
    errors = []
    
    # Validate emission values
    emission_fields = ['scope_1_emissions', 'scope_2_emissions', 'scope_3_emissions']
    for field in emission_fields:
        if field in data:
            value = data[field]
            if not isinstance(value, (int, float)) or value < 0:
                errors.append(f"{field} must be a non-negative number")
            elif value > 10000000:  # 10 million tonnes CO2e seems excessive
                errors.append(f"{field} value seems unrealistically high")
    
    # Validate reporting year
    if 'reporting_year' in data:
        year = data['reporting_year']
        current_year = datetime.now().year
        if not isinstance(year, int) or year < 2000 or year > current_year + 1:
            errors.append(f"Reporting year must be between 2000 and {current_year + 1}")
    
    return errors

def validate_weather_data(data: Dict[str, Any]) -> List[str]:
    """
    Validate weather data
    """
    errors = []
    
    # Validate temperature
    if 'temperature' in data:
        temp = data['temperature']
        if not isinstance(temp, (int, float)) or temp < -100 or temp > 70:
            errors.append("Temperature must be between -100°C and 70°C")
    
    # Validate humidity
    if 'humidity' in data:
        humidity = data['humidity']
        if not isinstance(humidity, (int, float)) or humidity < 0 or humidity > 100:
            errors.append("Humidity must be between 0% and 100%")
    
    # Validate pressure
    if 'pressure' in data:
        pressure = data['pressure']
        if not isinstance(pressure, (int, float)) or pressure < 800 or pressure > 1100:
            errors.append("Atmospheric pressure must be between 800 and 1100 hPa")
    
    # Validate wind speed
    if 'wind_speed' in data:
        wind_speed = data['wind_speed']
        if not isinstance(wind_speed, (int, float)) or wind_speed < 0 or wind_speed > 200:
            errors.append("Wind speed must be between 0 and 200 km/h")
    
    return errors
