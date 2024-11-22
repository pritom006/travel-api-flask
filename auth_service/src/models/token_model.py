import jwt
import datetime
from flask import current_app

# Secret key for signing the JWT tokens
SECRET_KEY = 'your_secret_key'

def generate_token(data):
    """
    Generate JWT token for the user
    """
    payload = {
        'email': data['email'],
        'role': data['role'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiry after 1 hour
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def validate_token(token):
    """
    Validate the JWT token and return the user info
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
