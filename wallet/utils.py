import jwt

def generate_custom_jwt_token(user):
    payload = {
        'user_id': user.id,
        # Другие данные, которые вы хотите включить в токен
    }
    return jwt.encode(payload, 'your-secret-key', algorithm='HS256')
