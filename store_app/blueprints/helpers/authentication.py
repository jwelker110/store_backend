from itsdangerous import URLSafeTimedSerializer, BadSignature
import random
import string
import os
import jwt


def generate_secret_key():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))


def generate_token(email, secretKey):

    serializer = URLSafeTimedSerializer(secret_key=secretKey)
    return serializer.dumps(email)


def confirm_token(token, secretKey):

    serializer = URLSafeTimedSerializer(secret_key=secretKey)
    try:
        email = serializer.loads(
                token,
                max_age=3600
        )
    except BadSignature:
        return False
    return email


def create_jwt(payload):
    key = os.environ.get('JWT_CIPHER')
    try:
        return jwt.encode(payload, key, algorithm='HS256')
    except:
        return None


def decode_jwt(jwt_token):
    key = os.environ.get('JWT_CIPHER')
    try:
        return jwt.decode(jwt_token, key, algorithm='HS256')
    except:
        return None
