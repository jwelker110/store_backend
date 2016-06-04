from base import StoreAppTestCase
from json import loads, dumps

from store_app.blueprints import decode_jwt
from store_app.database import Item


class TestItem(StoreAppTestCase):
    """
    Tests the Item related endpoints to ensure users are able to
    view, edit, and create items.
    """

    def setUp(self):
        super(TestItem, self).setUp()
        # perform some other set up here

    def test_getItems(self):
        req = self.client.get('/api/v1/items.json')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(10, len(items), 'Expected 10 items, retrieved %s.' % str(len(items)))

    def test_getItemsByOffset(self):
        req = self.client.get('/api/v1/items.json?offset=8')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(10, len(items), 'Expected 10 items, retrieved %s.' % str(len(items)))

    def test_getItemsByOffsetTooHigh(self):
        req = self.client.get('/api/v1/items.json?offset=99999999999')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(10, len(items), 'Expected 10 items, retrieved %s.' % str(len(items)))

    def test_getItemsByCategory(self):
        req = self.client.get('/api/v1/items.json?category=Other')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(10, len(items), 'Expected 10 items in \'Other\', retrieved %s.' % str(len(items)))

    def test_getItemsByCategoryNotExist(self):
        req = self.client.get('/api/v1/items.json?category=CategoryHerpDerp')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(0, len(items), 'Expected 0 items in \'CategoryHerpDerp\', retrieved %s.' % str(len(items)))

    def test_getItemsByCategoryOffset(self):
        req = self.client.get('/api/v1/items.json?category=Other&offset=19')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(1, len(items), 'Expected 1 item in \'Other\' when offset by 19, retrieved %s' % str(len(items)))

    def test_getItemsByCategoryNotExistOffsetTooHigh(self):
        req = self.client.get('/api/v1/items.json?category=CategoryHerpDerp&offset=9999999999')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(0, len(items), 'Expected 0 items in \'CategoryHerpDerp\', offset too high, retrieved %s.' % str(len(items)))

    def test_getItemInfo(self):
        req = self.client.get('/api/v1/items/details.json?name=Item1')
        data = loads(req.data)

        item = data.get('item')
        self.assertIsNotNone(item)

        self.assertIn('id', item, 'Item id not found in response.')
        self.assertIn('name', item, 'Item name not found in response.')
        self.assertIn('description', item, 'Item description not found in response.')
        self.assertIn('category', item, 'Item category not found in response.')
        self.assertIn('image_url', item, 'Item image_url not found in response.')
        self.assertIn('price', item, 'Item price not found in response.')
        self.assertIn('sale_price', item, 'Item sale_price not found in response.')
        self.assertIn('stock', item, 'Item stock not found in response.')
        self.assertIn('created_on', item, 'Item created_on not found in response.')
        self.assertIn('owner_name', item, 'Item owner_name not found in response.')

    def test_createItemWithoutPermissions(self):
        req = self.client.post('/api/v1/items.json', data=dumps({
            "name": "Item1234",
            "description": "This is the bestest item ever",
            "item_url": "image.jpg",
            "price": 2596,
            "sale_price": 1999,
            "stock": 1337,
        }))
        self.assertIn('401', req.status, 'Attempting to create an item without permission does not return 401 UNAUTHORIZED.')

    def test_updateItemWithoutPermission(self):
        req = self.client.put('/api/v1/items/details.json', data=dumps({
            "jwt_token": None,
            "name": "Item1",
            "description": "This is the new description",
            "image_url": "imageNoPermission.jpg",
            "price": 99.99,
            "sale_price": 99.98,
            "stock": 123,
        }))
        self.assertIn('401 UNAUTHORIZED', req.status,
                      'Updating an item without permission returns %s instead of 401 UNAUTHORIZED.' % req.status)

        req = self.client.get('/api/v1/items/details.json?name=Item1')
        data = loads(req.data)
        item = data.get('item')
        self.assertNotIn("imageNoPermission.jpg", item.get('image_url'), "Item was updated without required permission.")
