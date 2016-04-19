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
    recaptchaResponse = req.get('g-recaptcha-response')

    # the data to be returned to the client
    data = {
        "jwt_token": None
    }

    # todo uncomment when no longer testing
    # let's verify the user passed the recaptcha
    # r = requests.post('https://www.google.com/recaptcha/api/siteverify',
    #                   data=dict(secret=os.environ.get('RECAPTCHA_SECRET'), response=recaptchaResponse))
    # resp = r.json()
    #
    # if not resp['success']:  # they must be a robot or something
    #     return create_response({}, status=403)

    if email is None or username is None:
        return create_response({}, status=400)

    # check if the user already exists
    user = User.query.filter_by(username_lower=lower(username)).first()
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
            "confirmed": user.confirmed
        }
        jwt_token = create_jwt(payload)
        data['jwt_token'] = jwt_token

        # creates a confirmation email for the user based on their email and secret
        token = generate_token(user.email, user.confirm_secret)

        if send_confirmation_email(to=user.email, token=token):
            # the email was sent, let the user know
            return create_response(data)

        return create_response({}, status=500)

    except Exception as e:
        print e.message

        return create_response({}, status=500)


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Verify the user's credentials and return a JWT with the required claims
    :return: JWT with the claims for the user to be sent on future requests
    """
    req = loads(request.data)
    username = req.get('username')
    password = req.get('password')

    if username is None or password is None:
        return create_response({}, status=400)

    user = User.query.filter_by(username_lower=lower(username)).first()

    if user is None:
        return create_response({}, status=400)

    if user.check_password_hash(password):
        payload = {
            "username": user.username,
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
        user.confirmed = True
        db.session.commit()
        return create_response({})

    return create_response({}, status=400)


@auth_bp.route('/goauth', methods=['GET'])
def google_oauth():
    """
    Executes the auth flow required for google auth. If the user already has an account, they
    are signed in. If the user does not have an account, one is created for them and their account
    is automatically confirmed.
    :return: JWT with the claims for the user to be sent on future requests
    """
    flow = client.flow_from_clientsecrets(
        filename='store_app/blueprints/helpers/client_secrets.json',  # todo add these to environ var?
        scope='profile email',
        redirect_uri=url_for('auth_bp.google_oauth', _external=True)
    )

    if 'code' not in request.args:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)  # todo change this
        # return create_response({'uri': auth_uri})
    auth_code = request.args.get('code')
    credentials = flow.step2_exchange(auth_code)
    http_auth = credentials.authorize(httplib2.Http())
    resp = http_auth.request('https://www.googleapis.com/oauth2/v2/userinfo')
    userinfo = loads(resp[1])

    # if the account already exists, sign in, else create the account and sign in.
    user = User.query.filter_by(email_lower=userinfo.get('email')).first()
    if user is None:

        try:
            # create the account
            user = User(
                oa_id=userinfo.get('id'),
                first_name=userinfo.get('given_name'),
                last_name=userinfo.get('family_name'),
                email=userinfo.get('email'),
                username=split(userinfo.get('email'), '@')[0],
                confirmed=True
            )
            db.session.add(user)
            db.session.commit()

        except:
            return create_response({}, status=500)

    payload = {
        "username": user.username,
        "confirmed": user.confirmed
    }
    return create_response({
        "jwt_token": create_jwt(payload)
    })


@auth_bp.route('/foauth', methods=['GET'])
def facebook_oauth():
    # todo once front end is moving along a bit
    pass

