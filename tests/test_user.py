from base import StoreAppTestCase
from json import loads, dumps
from store_app.database import User


class TestUser(StoreAppTestCase):

    def setUp(self):
        super(TestUser, self).setUp()
        # perform some other set up here

    def test_userEndpointExists(self):
        self.endpointExists('/users')
        self.endpointExists('/user')

    def test_getUsers(self):
        req = self.client.get('/users')
        data = loads(req.data)
        self.assertEqual(10, len(data.get('users')), 'Did not retrieve all 3 users.')

    def test_getUsersByOffset(self):
        req = self.client.get('/users/8')
        data = loads(req.data)
        self.assertEqual(2, len(data.get('users')), 'Did not retrieve 2 users.')

    def test_getUserInfo(self):
        req = self.client.get('/user/Tester2')
        data = loads(req.data)
        userinfo = data.get('users')
        self.assertIn('username', userinfo, 'username not in userinfo')
        self.assertIn('items', userinfo, 'items not in userinfo')
        self.assertIn('registered_on', userinfo, 'registered_on not in userinfo')

    def test_getInvalidUserInfo(self):
        req = self.client.get('/user/ThisUserDoesNotExist')
        data = loads(req.data)
        userinfo = data.get('users')
        self.assertEqual(0, len(userinfo), 'Unexpected user info present in response.')

    def test_getUserItems(self):
        req = self.client.get('/user/Tester2/items')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(10, len(items), 'Did not retrieve 10 items associated with Tester2.')

    def test_getUserItemsByOffset(self):
        req = self.client.get('/user/Tester2/items/8')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(2, len(items), 'Did not retrieve 2 items associated with Tester2.')

    def test_getInvalidUserItems(self):
        req = self.client.get('/user/ThisUserDoesNotExist/items')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(0, len(items), 'Unexpected item(s) present in response.')

    def test_createUser(self):
        with self.app.mail.record_messages() as outbox:
            req = self.client.post('/user', content_type=self.ctype, data=dumps({
                'username': 'Tester11',
                'email': 'Tester11@email.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'password': 'lol123'
            }))
            data = loads(req.data)
            self.assertIsNotNone(data.get('jwt_token'), 'JWT token not present in response.')
            user = User.query.filter(username='Tester11').first()
            self.assertIsNotNone(user, 'User was not created.')


