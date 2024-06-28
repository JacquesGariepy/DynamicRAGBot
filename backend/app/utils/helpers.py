import re

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def sanitize_input(input_string):
    return re.sub(r'[^\w\s-]', '', input_string).strip()

def generate_password_hash(password):
    # This is a placeholder. In a real application, use a proper password hashing library
    return hash(password)

def check_password_hash(hashed_password, password):
    # This is a placeholder. In a real application, use a proper password hashing library
    return hashed_password == hash(password)