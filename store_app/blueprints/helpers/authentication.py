import os
import jwt
from datetime import datetime, timedelta


def create_jwt(payload):
    key = os.environ.get('JWT_CIPHER')
    try:
        payload['iat'] = datetime.utcnow()
        payload['exp'] = datetime.utcnow() + timedelta(days=3)
        return jwt.encode(payload, key, algorithm='HS256')
    except:
        return None


def decode_jwt(jwt_token):
    key = os.environ.get('JWT_CIPHER')
    try:
        return jwt.decode(jwt_token, key, algorithm='HS256')
    except:
        return None
