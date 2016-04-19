from base import StoreAppTestCase
from json import loads, dumps

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
