"""
Input validation utilities and custom validators for Palace of Quests.
Provides reusable validation logic with comprehensive error handling.

Author: Senior Backend Team  
Last Modified: 2025-06-04
"""

import re
import datetime
from typing import Any, Dict, List, Optional, Union, Callable
from flask import request
from marshmallow import Schema, fields, validate, ValidationError, pre_load
from email_validator import validate_email, EmailNotValidError


class ValidationMixin:
    """Mixin class providing common validation utilities."""
    
    @staticmethod
    def validate_password_strength(password: str) -> bool:
        """
        Validate password meets security requirements.
        
        Requirements:
        - At least 8 characters
        - Contains uppercase letter
        - Contains lowercase letter  
        - Contains digit
        - Contains special character
        """
        if len(password) < 8:
            return False
        
        patterns = [
            r'[A-Z]',  # Uppercase
            r'[a-z]',  # Lowercase
            r'\d',     # Digit
            r'[!@#$%^&*(),.?":{}|<>]'  # Special characters
        ]
        
        return all(re.search(pattern, password) for pattern in patterns)
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """Validate username format and content."""
        if not username or len(username) < 3 or len(username) > 30:
            return False
        
        # Allow alphanumeric, underscore, hyphen
        pattern = r'^[a-zA-Z0-9_-]+$'
        return bool(re.match(pattern, username))
    
    @staticmethod
    def sanitize_html_input(text: str) -> str:
        """Basic HTML sanitization for user input."""
        if not text:
            return ""
        
        # Remove potentially dangerous HTML tags
        dangerous_tags = [
            '<script', '</script>', '<iframe', '</iframe>',
            '<object', '</object>', '<embed', '</embed>',
            '<form', '</form>', 'javascript:', 'vbscript:',
            'onload=', 'onerror=', 'onclick='
        ]
        
        cleaned_text = text
        for tag in dangerous_tags:
            cleaned_text = re.sub(tag, '', cleaned_text, flags=re.IGNORECASE)
        
        return cleaned_text.strip()


# Custom validator functions
def validate_currency_amount(value: float) -> float:
    """Validate currency amount is positive and has max 2 decimal places."""
    if value < 0:
        raise ValidationError("Amount must be positive")
    
    # Check decimal places
    if round(value, 2) != value:
        raise ValidationError("Amount cannot have more than 2 decimal places")
    
    if value > 999999.99:
        raise ValidationError("Amount exceeds maximum allowed value")
    
    return value


def validate_quest_difficulty(value: int) -> int:
    """Validate quest difficulty level."""
    if not isinstance(value, int) or value < 1 or value > 10:
        raise ValidationError("Difficulty must be an integer between 1 and 10")
    return value


def validate_file_upload(file_data: Any) -> bool:
    """Validate uploaded file meets requirements."""
    if not hasattr(file_data, 'filename'):
        raise ValidationError("Invalid file upload")
    
    # Check file extension
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx'}
    file_ext = file_data.filename.lower().split('.')[-1] if '.' in file_data.filename else ''
    
    if f'.{file_ext}' not in allowed_extensions:
        raise ValidationError(f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}")
    
    # Check file size (5MB limit)
    if hasattr(file_data, 'content_length') and file_data.content_length > 5 * 1024 * 1024:
        raise ValidationError("File size exceeds 5MB limit")
    
    return True


# Schema definitions
class UserRegistrationSchema(Schema, ValidationMixin):
    """Schema for user registration validation."""
    
    username = fields.Str(required=True, validate=validate.Length(min=3, max=30))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    terms_accepted = fields.Bool(required=True)
    
    @pre_load
    def preprocess_data(self, data, **kwargs):
        """Clean and preprocess input data."""
        if isinstance(data, dict):
            # Sanitize text fields
            text_fields = ['username', 'first_name', 'last_name']
            for field in text_fields:
                if field in data and isinstance(data[field], str):
                    data[field] = self.sanitize_html_input(data[field])
        return data
    
    def validate_username(self, value):
        """Custom username validation."""
        if not self.validate_username(value):
            raise ValidationError("Username must be 3-30 characters, alphanumeric with _ or - allowed")
    
    def validate_password(self, value):
        """Custom password validation."""
        if not self.validate_password_strength(value):
            raise ValidationError(
                "Password must be at least 8 characters with uppercase, lowercase, digit, and special character"
            )
    
    def validate_terms_accepted(self, value):
        """Ensure terms are accepted."""
        if not value:
            raise ValidationError("Terms and conditions must be accepted")


class QuestCreationSchema(Schema, ValidationMixin):
    """Schema for quest creation validation."""
    
    title = fields.Str(required=True, validate=validate.Length(min=5, max=100))
    description = fields.Str(required=True, validate=validate.Length(min=10, max=1000))
    difficulty = fields.Int(required=True, validate=validate_quest_difficulty)
    reward_amount = fields.Float(required=True, validate=validate_currency_amount)
    category = fields.Str(required=True, validate=validate.OneOf([
        'combat', 'exploration', 'crafting', 'social', 'puzzle', 'collection'
    ]))
    requirements = fields.List(fields.Str(), missing=[])
    time_limit_hours = fields.Int(missing=None, allow_none=True, validate=validate.Range(min=1, max=168))
    max_participants = fields.Int(missing=None, allow_none=True, validate=validate.Range(min=1, max=100))
    
    @pre_load
    def preprocess_quest_data(self, data, **kwargs):
        """Clean quest input data."""
        if isinstance(data, dict):
            # Sanitize text fields
            text_fields = ['title', 'description']
            for field in text_fields:
                if field in data and isinstance(data[field], str):
                    data[field] = self.sanitize_html_input(data[field])
        return data


class TransactionSchema(Schema):
    """Schema for transaction validation."""
    
    amount = fields.Float(required=True, validate=validate_currency_amount)
    transaction_type = fields.Str(required=True, validate=validate.OneOf([
        'quest_reward', 'marketplace_purchase', 'marketplace_sale', 
        'transfer', 'bonus', 'penalty'
    ]))
    description = fields.Str(missing="", validate=validate.Length(max=200))
    recipient_id = fields.Int(missing=None, allow_none=True)
    reference_id = fields.Str(missing=None, allow_none=True)


class PaginationSchema(Schema):
    """Schema for pagination parameters."""
    
    page = fields.Int(missing=1, validate=validate.Range(min=1, max=1000))
    per_page = fields.Int(missing=20, validate=validate.Range(min=1, max=100))
    sort_by = fields.Str(missing='created_at')
    sort_order = fields.Str(missing='desc', validate=validate.OneOf(['asc', 'desc']))


def validate_request_json(schema_class: Schema) -> Callable:
    """
    Decorator to validate JSON request data against a schema.
    
    Args:
        schema_class: Marshmallow schema class for validation
        
    Returns:
        Decorator function
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not request.is_json:
                raise ValidationError("Request must contain JSON data")
            
            schema = schema_class()
            try:
                validated_data = schema.load(request.get_json())
                # Add validated data to request context
                request.validated_json = validated_data
                return func(*args, **kwargs)
            except ValidationError as e:
                raise ValidationError(f"Request validation failed: {e.messages}")
        
        return wrapper
    return decorator


def validate_query_params(schema_class: Schema) -> Callable:
    """
    Decorator to validate query parameters against a schema.
    
    Args:
        schema_class: Marshmallow schema class for validation
        
    Returns:
        Decorator function  
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            schema = schema_class()
            try:
                validated_params = schema.load(request.args.to_dict())
                request.validated_args = validated_params
                return func(*args, **kwargs)
            except ValidationError as e:
                raise ValidationError(f"Query parameter validation failed: {e.messages}")
        
        return wrapper
    return decorator
