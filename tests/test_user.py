from base import StoreAppTestCase
from json import loads


class TestUser(StoreAppTestCase):

    def setUp(self):
        super(TestUser, self).setUp()
        # perform some other set up here

    def test_getUsers(self):
        req = self.client.get('/api/v1/users.json')
        data = loads(req.data)
        self.assertEqual(10, len(data.get('users')), 'Did not retrieve all 10 users. Retrieved %s' % str(len(data.get('users'))))

    def test_getUsersByOffset(self):
        req = self.client.get('/api/v1/users.json?offset=8')
        data = loads(req.data)
        self.assertEqual(2, len(data.get('users')), 'Did not retrieve 2 users. Retrieved %s' % str(len(data.get('users'))))

    def test_getUserItems(self):
        req = self.client.get('/api/v1/users/items.json?username=Tester2')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(2, len(items), 'Did not retrieve 2 items associated with Tester2. Retrieved %s' % str(len(items)))

    def test_getUserItemsByOffset(self):
        req = self.client.get('/api/v1/users/items.json?username=Tester2&offset=1')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(1, len(items), 'Did not retrieve 1 item associated with Tester2. Retrieved %s' % str(len(items)))

    def test_getInvalidUserItems(self):
        req = self.client.get('/api/v1/users/items.json?username=DoesNotExist')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(0, len(items), 'Unexpected item(s) present in response.')
