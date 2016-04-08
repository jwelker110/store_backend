from itsdangerous import URLSafeTimedSerializer, BadSignature
import random
import string


def generate_secret_key():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))


def generate_confirm_token(email, secretKey):

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

