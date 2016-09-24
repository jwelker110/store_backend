from flask import Blueprint, request
from json import loads
from string import lower, split
import httplib2

from oauth2client import client, crypt

from store_app.database import User
from helpers import create_response, create_jwt, decode_jwt
from store_app.extensions import db

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route('/api/reauth', methods=['POST'])
def jwt_reauth():
    """
    Reauthenticates the provided JWT Token
    :return: JWT with the claims for the user to be sent on future requests
    """

    req = loads(request.data)
    jwt_token = req.get('jwt_token')

    payload = decode_jwt(jwt_token)

    if payload is None:
        return create_response({}, status=401)

    return create_response({'jwt_token': create_jwt(payload)})


@auth_bp.route('/api/goauth', methods=['POST'])
def google_oauth():
    """
    If the user already has an account, they are signed in. If the user does 
    not have an account, one is created for them and their account is 
    automatically confirmed.
    :return: JWT with the claims for the user to be sent on future requests
    """

    data = loads(request.data)
    access_token = data.get('access_token')

    if access_token is None:
        return create_response({}, status=400)

    try:
        # we are going to try to use this access token to retrieve the user's
        # info and create their account.
        cred = client.AccessTokenCredentials(access_token, 'Store-App/v1')
        http = cred.authorize(httplib2.Http())

        r = http.request('https://www.googleapis.com/oauth2/v3/userinfo')
        resp = loads(r[1])
    except:
        return create_response({}, status=500)

    # so we were able to get user's info, let's make sure we
    # have the correct info
    email = resp.get('email')
    oa_id = resp.get('sub')  # per Google, equiv to user ID

    # can't create a blank account now, can we?
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

    # the user is signed in so let's return a JWT with their info!
    payload = {
        "username": user.username,
        "isOauth": True,
        "confirmed": user.confirmed
    }

    return create_response({
        "jwt_token": create_jwt(payload)
    })
