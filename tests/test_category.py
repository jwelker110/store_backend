from base import StoreAppTestCase
from json import loads


class TestCategory(StoreAppTestCase):

    def setUp(self):
        super(TestCategory, self).setUp()
        # perform some other set up here

    def test_categoryEndpointExists(self):
        self.endpointExists('/categories')

    def test_getCategories(self):
        req = self.client.get('/categories')
        data = loads(req.data)
        cats = data.get('categories')
        self.assertEqual(5, len(cats), 'Did not retrieve 5 categories.')

    def test_getCategoryItems(self):
        req = self.client.get('/categories/Electronics/items')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(1, len(items), 'Did not retrieve 1 items from category Electronics.')

    def test_getCategoryItemsByOffset(self):
        req = self.client.get('/categories/Electronics/items/1')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(1, len(items), 'Did not retrieve 1 item from category Electronics.')

    def test_getCategoryItemsByUser(self):
        req = self.client.get('/categories/Electronics/user/Tester2')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(2, len(items), 'Did not retrieve 2 items from category Electronics associated with user Tester2')