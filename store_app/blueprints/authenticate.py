from flask import Blueprint, request, url_for, redirect
from json import loads
from string import lower, split
import httplib2

from store_app.database import User
from helpers import create_response, send_confirmation_email, generate_token, create_jwt, decode_jwt, confirm_token
from store_app.extensions import db

from oauth2client import client

auth_bp = Blueprint("auth_bp", __name__)


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

