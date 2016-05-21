from base import StoreAppTestCase
from json import loads, dumps
from datetime import datetime
import time

from store_app.blueprints import decode_jwt
from store_app.database import User


class TestAuthenticate(StoreAppTestCase):
    """
    Tests the authentication endpoints of the application to ensure users are able to
    register, login, re-authenticate
    """

    def setUp(self):
        super(TestAuthenticate, self).setUp()

    # todo rewrite test register user

    # todo rewrite test already registered

    # todo rewrite test login

    # todo rewrite test reauth