from flask import Blueprint, request
from json import loads
import jwt
import requests
import os

from store_app.database import User
from helpers import create_response, send_confirmation_email, generate_token, create_jwt
from store_app.extensions import db

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Create a new user account using the supplied user info and send a confirmation email to the user.
    Integrated recaptcha prevents excessive calls to register user accounts
    :return: JWT with the user credentials enclosed
    """

    firstName = request.form.get('first_name')
    lastName = request.form.get('last_name')
    email = request.form.get('email')
    username = request.form.get('username')
    recaptchaResponse = request.form.get('g-recaptcha-response')

    # the data to be returned to the client
    data = {
        "jwt_token": None,
        "msg": None
    }

    # let's verify the user passed the recaptcha
    r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                      data=dict(secret=os.environ.get('RECAPTCHA_SECRET'), response=recaptchaResponse))
    resp = r.json()

    if not resp['success']:  # they must be a robot or something
        return create_response({}, status=403)

    if email is None or username is None:
        return create_response({}, status=400)

    try:

        user = User(
            first_name=firstName,
            last_name=lastName,
            email=email,
            username=username
        )
        db.session.add(user)
        db.session.commit()

        payload = {
            "username": user.username,
            "confirmed": user.confirmed
        }
        jwt_token = create_jwt(payload)
        data['jwt_token'] = jwt_token

        # creates a confirmation email for the user based on their email and secret
        token = generate_token(user.email, user.confirm_secret)

        if send_confirmation_email(to=user.email, token=token):
            # the email was sent, let the user know
            return create_response(data)

        data['msg'] = "Unable to send confirmation email at this time. Try again later."
        return create_response(data, status=500)

    except Exception as e:
        print e.message

        # unable to add the user
        data['msg'] = "Unable to create your account at this time. Try again later."
        return create_response(data, status=500)


@auth_bp.route('/login', methods=['POST'])
def login():
    pass


@auth_bp.route('/confirm', methods=['POST'])
def confirm():
    pass


@auth_bp.route('/register_google', methods=['POST'])
def register_google():
    pass


@auth_bp.route('/login_google', methods=['POST'])
def login_google():
    pass


@auth_bp.route('/register_facebook', methods=['POST'])
def register_facebook():
    pass


@auth_bp.route('/login_facebook', methods=['POST'])
def login_facebook():
    pass
