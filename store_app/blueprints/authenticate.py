from flask import Blueprint, request, url_for, redirect
from json import loads
from string import lower, split
import httplib2

from store_app.database import User
from helpers import create_response, send_confirmation_email, generate_token, create_jwt, decode_jwt, confirm_token
from store_app.extensions import db

from oauth2client import client

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Create a new user account using the supplied user info and send a confirmation email to the user.
    Integrated recaptcha prevents excessive calls to register user accounts
    :return: JWT with the user credentials enclosed
    """
    req = loads(request.data)
    firstName = req.get('first_name')
    lastName = req.get('last_name')
    email = req.get('email')
    username = req.get('username')
    password = req.get('password')
    recaptchaResponse = req.get('g_recaptcha_response')

    # todo uncomment when no longer testing
    # let's verify the user passed the recaptcha
    # r = requests.post('https://www.google.com/recaptcha/api/siteverify',
    #                   data=dict(secret=os.environ.get('RECAPTCHA_SECRET'), response=recaptchaResponse))
    # resp = r.json()
    #
    # if not resp['success']:  # they must be a robot or something
    #     return create_response({}, status=403)

    if email is None or password is None:
        return create_response({}, status=400)

    # check if the user already exists
    user = User.query.filter_by(email_lower=lower(email)).first()
    if user is not None:  # todo maybe I should return error messages?
        return create_response({}, status=409)

    try:

        user = User(
            first_name=firstName,
            last_name=lastName,
            email=email,
            username=username,
            password=password
        )
        db.session.add(user)
        db.session.commit()

        payload = {
            "username": user.username,
            "isOauth": False,
            "avatarUrl": user.avatar_url,
            "confirmed": user.confirmed
        }

        # creates a confirmation email for the user based on their email and secret
        token = generate_token(user.email, user.confirm_secret)

        if send_confirmation_email(to=user.email, token=token):
            # the email was sent, let the user know
            return create_response({
                "jwt_token": create_jwt(payload)
                })

        return create_response({
            "jwt_token": create_jwt(payload)
            }, status=500)

    except Exception as e:
        db.session.rollback()
        return create_response({}, status=500)


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Verify the user's credentials and return a JWT with the required claims
    :return: JWT with the claims for the user to be sent on future requests
    """
    req = loads(request.data)
    email = req.get('email')
    password = req.get('password')

    if email is None or password is None:
        return create_response({}, status=400)

    user = User.query.filter_by(email_lower=lower(email)).first()

    if user is None:
        return create_response({}, status=400)

    if user.check_password_hash(password):
        payload = {
            "username": user.username,
            "isOauth": False,
            "avatarUrl": user.avatar_url,
            "confirmed": user.confirmed
        }
        return create_response({
            "jwt_token": create_jwt(payload)
        })
    return create_response({}, status=400)


@auth_bp.route('/confirm', methods=['POST'])
def confirm():
    """
    Confirm the account associated with the supplied confirmation code
    :return: JWT with the claims for the user to be sent on future requests
    """
    req = loads(request.data)
    token = req.get('confirm_token')
    # grab the JWT
    jwt_token = req.get('jwt_token')
    # grab the JWT payload
    payload = decode_jwt(jwt_token)
    # grab the JWT payload contents
    username = payload.get('username')
    confirmed = payload.get('confirmed')

    user = User.query.filter_by(username_lower=lower(username)).first()

    if user is None or confirmed:
        return create_response({}, status=400)

    email = confirm_token(token, user.confirm_secret)

    if email:
        try:
            user.confirmed = True
            db.session.commit()
            return create_response({})
        except:
            db.session.rollback()
            return create_response({}, status=500)

    return create_response({}, status=400)


@auth_bp.route('/reauth', methods=['POST'])
def jwt_reauth():

    req = loads(request.data)
    jwt_token = req.get('jwt_token')

    payload = decode_jwt(jwt_token)

    if payload is None:
        return create_response({}, status=401)

    return create_response({'jwt_token': create_jwt(payload)})


@auth_bp.route('/goauth', methods=['POST'])
def google_oauth():
    """
    If the user already has an account, they are signed in. If the user does 
    not have an account, one is created for them and their account is 
    automatically confirmed.
    :return: JWT with the claims for the user to be sent on future requests
    """

    req = loads(request.data)
    email = req.get('email')
    oa_id = req.get('oa_id')

    if email is None or oa_id is None:
        return create_response({}, status=400)

    # if the account already exists, sign in, else create the account and sign in.
    user = User.query.filter_by(email_lower=lower(email)).first()
    if user is None:

        try:
            # create the account
            user = User(
                oa_id=oa_id,
                email=email,
                username=split(email, '@')[0],
                confirmed=True
            )
            db.session.add(user)
            db.session.commit()

        except:
            db.session.rollback()
            return create_response({}, status=500)

    payload = {
        "username": user.username,
        "isOauth": True,
        "avatarUrl": user.avatar_url,
        "confirmed": user.confirmed
    }
    return create_response({
        "jwt_token": create_jwt(payload)
    })


@auth_bp.route('/foauth', methods=['GET'])
def facebook_oauth():
    # todo once front end is moving along a bit
    pass

