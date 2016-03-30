from base import StoreAppTestCase
from json import loads, dumps


class TestItem(StoreAppTestCase):

    def setUp(self):
        super(TestItem, self).setUp()
        # perform some other set up here

    def test_itemEndpointExists(self):
        self.endpointExists('/items')

    def test_getItems(self):
        req = self.client.get('/items')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(10, len(items), 'Did not retrieve 10 items.')

    def test_getItemsByOffset(self):
        req = self.client.get('/items/8')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(2, len(items), 'Did not retrieve 2 items.')

    def test_getItemInfo(self):
        req = self.client.get('/item/ItemName')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(1, len(items), 'Did not retrieve item information for 1 specific item.')
        for item in items:
            self.assertIn('name', item, 'Item name not found in response.')
            self.assertIn('description', item, 'Item description not found in response.')
            self.assertIn('price', item, 'Item price not found in response.')
            self.assertIn('discount', item, 'Item discount not found in response.')
            self.assertIn('sale_price', item, 'Item sale_price not found in response.')
            self.assertIn('stock', item, 'Item stock not found in response.')
            self.assertIn('created_on', item, 'Item created_on not found in response.')
            self.assertIn('creator_name', item, 'Item creator_name not found in response.')
            self.assertIn('category', item, 'Item category not found in response.')

    def test_createItem(self):
        # todo will need to get JWT token from signing in and then send it along with this request
        req = self.client.post('/item', content_type=self.ctype, data=dumps({

        }))
