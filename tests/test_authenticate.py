from base import StoreAppTestCase
from json import loads, dumps
from datetime import datetime
import time

from store_app.blueprints import decode_jwt
from store_app.database import User


class TestAuthenticate(StoreAppTestCase):

    def setUp(self):
        super(TestAuthenticate, self).setUp()

    def test_registerUser(self):
        # with self.app.mail.record_messages() as outbox:
        req = self.client.post('/register', content_type=self.ctype, data=dumps({
            'username': 'Tester11',
            'email': 'Tester11@email.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'lol123'
        }))
        data = loads(req.data)
        self.assertIn('jwt_token', data, 'JWT token not present in response.')
        user = User.query.filter_by(username='Tester11').first()
        self.assertIsNotNone(user, 'User was not created.')
        # self.assertGreater(0, len(outbox), 'No emails have been captured via outbox.')

    def test_registerUserAlreadyRegistered(self):
        req = self.client.post('/register', content_type=self.ctype, data=dumps({
            'username': 'Tester1',
            'email': 'Tester1@email.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'lol123'
        }))
        self.assertIn('409', req.status, 'Attempting to create an account that already exists does not return 409 Conflict.')

    def test_loginUser(self):
        req = self.client.post('/login', content_type=self.ctype, data=dumps({
            'username': 'Tester1',
            'password': 'lol123'
        }))
        data = loads(req.data)
        self.assertIn('jwt_token', data, 'JWT token not present in response.')
        payload = decode_jwt(data.get('jwt_token'))
        self.assertIn('username', payload, 'Username attribute not in JWT.')
        self.assertIn('confirmed', payload, 'Confirmed attribute not in JWT.')

    def test_reauthUser(self):
        req = self.client.post('/login', content_type=self.ctype, data=dumps({
            'username': 'Tester1',
            'password': 'lol123'
        }))
        data = loads(req.data)
        jwt_token = data.get('jwt_token')
        payload = decode_jwt(jwt_token)
        iat = payload.get('iat')

        time.sleep(1)

        req = self.client.post('/reauth', content_type=self.ctype, data=dumps({
            'jwt_token': jwt_token
        }))
        data = loads(req.data)
        jwt_token = data.get('jwt_token')
        payload = decode_jwt(jwt_token)
        newiat = payload.get('iat')

        self.assertGreater(newiat, iat, 'New token iat timestamp is from earlier than old iat timestap (Old token: %s | New token: %s)' % (iat, newiat))
