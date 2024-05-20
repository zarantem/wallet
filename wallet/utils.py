import jwt
from .settings import JWT

def generate_custom_jwt_token(user):
    payload = {
        'user_id': user.id,
        # Другие данные, которые вы хотите включить в токен
    }
    return jwt.encode(payload, JWT, algorithm='HS256')
