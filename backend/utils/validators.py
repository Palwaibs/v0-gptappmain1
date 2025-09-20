import re
import phonenumbers
from email_validator import validate_email, EmailNotValidError
from flask import current_app

def validate_email_format(email):
    """Validate email format using email-validator library"""
    try:
        valid = validate_email(email)
        return True, valid.email
    except EmailNotValidError as e:
        return False, str(e)

def validate_phone_number(phone):
    """Validate phone number format using phonenumbers library"""
    if not phone:
        return True, phone  # Phone is optional
    
    try:
        # Parse phone number (assuming Indonesian numbers if no country code)
        if phone.startswith('+'):
            parsed = phonenumbers.parse(phone, None)
        elif phone.startswith('0'):
            parsed = phonenumbers.parse(phone, 'ID')
        else:
            parsed = phonenumbers.parse('+62' + phone, None)
        
        if phonenumbers.is_valid_number(parsed):
            return True, phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        else:
            return False, "Invalid phone number format"
    except phonenumbers.NumberParseException as e:
        return False, f"Phone number parse error: {str(e)}"

def validate_package_id(package_id):
    """Validate if package_id exists in configuration"""
    packages = current_app.config.get('PACKAGES', {})
    if package_id not in packages:
        return False, f"Invalid package_id: {package_id}"
    return True, package_id

def sanitize_input(text):
    """Basic input sanitization"""
    if not text:
        return text
    
    # Remove potentially dangerous characters
    text = re.sub(r'[<>"\']', '', str(text))
    # Limit length
    text = text[:255]
    # Strip whitespace
    text = text.strip()
    
    return text

def validate_order_data(data):
    """Comprehensive validation for order data"""
    errors = {}
    
    # Required fields
    required_fields = ['customer_email', 'package_id']
    for field in required_fields:
        if field not in data or not data[field]:
            errors[field] = f"{field} is required"
    
    # Email validation
    if 'customer_email' in data and data['customer_email']:
        is_valid, result = validate_email_format(data['customer_email'])
        if not is_valid:
            errors['customer_email'] = result
        else:
            data['customer_email'] = result
    
    # Package validation
    if 'package_id' in data and data['package_id']:
        is_valid, result = validate_package_id(data['package_id'])
        if not is_valid:
            errors['package_id'] = result
    
    # Phone validation (optional)
    if 'phone_number' in data and data['phone_number']:
        is_valid, result = validate_phone_number(data['phone_number'])
        if not is_valid:
            errors['phone_number'] = result
        else:
            data['phone_number'] = result
    
    # Handle alternative field names
    if 'phone' in data and not data.get('phone_number'):
        data['phone_number'] = data['phone']
    
    if 'name' in data and not data.get('full_name'):
        data['full_name'] = data['name']
    
    # Sanitize optional text fields
    if 'full_name' in data:
        data['full_name'] = sanitize_input(data['full_name'])
    
    if 'name' in data:
        data['name'] = sanitize_input(data['name'])
    
    return len(errors) == 0, errors, data
