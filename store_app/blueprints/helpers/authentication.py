import os
import jwt
from datetime import datetime, timedelta


def create_jwt(payload):
    """
    Creates a JWT with the provided payload or returns None
    :param payload: The dict to encode
    :return: the JWT, or None
    """
    key = os.environ.get('JWT_CIPHER')
    try:
        payload['iat'] = datetime.utcnow()
        payload['exp'] = datetime.utcnow() + timedelta(days=3)
        return jwt.encode(payload, key, algorithm='HS256')
    except:
        return None


def decode_jwt(jwt_token):
    """
    Decodes a JWT from the provided token or returns None
    :param jwt_token: The JWT Token string
    :return: The payload, or None
    """
    key = os.environ.get('JWT_CIPHER')
    try:
        return jwt.decode(jwt_token, key, algorithm='HS256')
    except:
        return None
