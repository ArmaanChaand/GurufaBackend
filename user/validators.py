import random 
import string
import re
from django.core.exceptions import ValidationError

def password_validator(password):
    # Check if password is at least 8 characters long
    if len(password) < 8:
        return [False, 'Password must be at least 8 characters long.']
    
    # Check if password contains at least one uppercase letter
    if not re.search(r"[A-Z]", password):
        return [False, "Password must contain at least one uppercase letter."]
    
    # Check if password contains at least one lowercase letter
    if not re.search(r"[a-z]", password):
        return  [False, "Password must contain at least one lowercase letter."]
    
    # Check if password contains at least one digit
    if not re.search(r"\d", password):
        return [False, "Password must contain at least one digit."]
    
    # Check if password contains at least one special character
    if not re.search(r"[!@#$%^&*()_+=\-[\]{};':\"|,.<>/?]", password):
        return [False, "Password must contain at least one special character."]
    
    # Password meets all criteria
    return [True, password]

def generate_strong_password(length=12):
    """
    Generate a strong password that passes the password_validator function.

    :param length: Length of the password (default: 12)
    :return: Strong password that meets the criteria
    """
    while True:
        password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))
        validation_result = password_validator(password)
        if validation_result[0]:
            return validation_result[1]


def validate_kids_age(age):
    if not (5 <= age <= 15):
        raise ValidationError("Kid's age must be between 2 and 15.")

