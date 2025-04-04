from functools import wraps
from flask import request, jsonify
import jwt
from app.config import Config


def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({'error': 'Authorization header missing'}), 401

            try:
                token = auth_header.split(" ")[1]
                decoded_token = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
                user_role = decoded_token.get('role')

                if user_role != required_role:
                    return jsonify({'error': 'Unauthorized access: role mismatch'}), 403

            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Invalid token'}), 401
            except Exception as e:
                return jsonify({'error': str(e)}), 500

            return f(*args, **kwargs)
        return wrapper
    return decorator
