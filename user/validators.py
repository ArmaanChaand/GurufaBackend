import re

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
