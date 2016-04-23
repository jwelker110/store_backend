from base import StoreAppTestCase
from json import loads, dumps

from store_app.blueprints import decode_jwt
from store_app.database import Item, ItemMeta


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
        self.assertEqual(20, len(items), 'Expected 20 items, retrieved %s.' % str(len(items)))

    def test_getItemsByOffset(self):
        req = self.client.get('/api/v1/items.json?offset=8')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(12, len(items), 'Expected 12 items, retrieved %s.' % str(len(items)))

    def test_getItemsByOffsetTooHigh(self):
        req = self.client.get('/api/v1/items.json?offset=99999999999')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(20, len(items), 'Expected 20 items, retrieved %s.' % str(len(items)))

    def test_getItemsByCategory(self):
        req = self.client.get('/api/v1/items.json?category=Category1')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(2, len(items), 'Expected 2 items in \'Category1\', retrieved %s.' % str(len(items)))

    def test_getItemsByCategoryNotExist(self):
        req = self.client.get('/api/v1/items.json?category=CategoryHerpDerp')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(0, len(items), 'Expected 0 items in \'CategoryHerpDerp\', retrieved %s.' % str(len(items)))

    def test_getItemsByCategoryOffset(self):
        req = self.client.get('/api/v1/items.json?category=Category1&offset=1')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(1, len(items), 'Expected 1 item in \'Category1\' when offset by 1, retrieved %s' % str(len(items)))

    def test_getItemsByCategoryNotExistOffsetTooHigh(self):
        req = self.client.get('/api/v1/items.json?category=CategoryHerpDerp&offset=9999999999')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(0, len(items), 'Expected 0 items in \'CategoryHerpDerp\', offset too high, retrieved %s.' % str(len(items)))

    def test_getItemInfo(self):
        req = self.client.get('/api/v1/items/details.json?name=Item1')
        data = loads(req.data)

        items = data.get('items')
        itemMeta = data.get('item_meta')
        self.assertEqual(1, len(items), 'Expected information for 1 item, got information for %s items.' % str(len(items)))

        for item in items:
            self.assertIn('id', item, 'Item id not found in response.')
            self.assertIn('name', item, 'Item name not found in response.')
            self.assertIn('description', item, 'Item description not found in response.')

        for meta in itemMeta:
            self.assertIn('id', meta, "ItemMeta id not found in response.")
            self.assertIn('item_id', meta, 'ItemMeta item_id not found in response.')
            self.assertIn('image_url', meta, 'ItemMeta image_url not found in response.')
            self.assertIn('price', meta, 'ItemMeta price not found in response.')
            self.assertIn('sale_price', meta, 'ItemMeta sale_price not found in response.')
            self.assertIn('stock', meta, 'ItemMeta stock not found in response.')
            self.assertIn('created_on', meta, 'ItemMeta created_on not found in response.')
            self.assertIn('description', meta, 'ItemMeta description not found in response.')
            self.assertIn('meta_key', meta, 'ItemMeta key not found in response.')
            self.assertIn('meta_value', meta, 'ItemMeta value not found in response.')

    def test_createItem(self):
        # first login and retrieve the jwt
        req = self.client.post('/login', data=dumps({
            'username': 'Tester1',
            'password': 'lol123'
        }))
        data = loads(req.data)
        jwt_token = data.get('jwt_token')

        req = self.client.post('/api/v1/items.json', data=dumps({
            "jwt_token": jwt_token,
            "name": "Item123",
            "description": "This is the best item ever",
            "price": 2596,
            "sale_price": 1999,
            "stock": 1337,
            "meta_description": "This is the default item description",
            "meta_key": "Color",
            "meta_value": "Black"
        }))
        self.assertEqual(req.status, '200 OK', "Creating an item returned status %s" % str(req.status))

        item = Item.query.filter_by(name='Item123').first()
        self.assertIsNotNone(item, 'Item123 was not created.')
        itemMeta = ItemMeta.query.filter_by(item_id=item.id).first()
        self.assertIsNotNone(itemMeta, 'Item123 Meta was not created.')

    def test_createItemWithoutPermissions(self):
        req = self.client.post('/api/v1/items.json', data=dumps({
            "name": "Item1234",
            "description": "This is the bestest item ever",
            "price": 2596,
            "sale_price": 1999,
            "stock": 1337,
            "meta_description": "This should not have been created.",
            "meta_key": "Color",
            "meta_value": "Black"
        }))
        self.assertIn('401', req.status, 'Attempting to create an item without permission does not return 401 UNAUTHORIZED.')

    def test_updateItem(self):
        req = self.client.post('/login', content_type=self.ctype, data=dumps({
            'username': 'Tester1',
            'password': 'lol123'
        }))
        data = loads(req.data)
        jwt_token = data.get('jwt_token')

        req = self.client.put('/api/v1/items/details.json', data=dumps({
            "jwt_token": jwt_token,
            "name": "Item1",
            "description": "This is the new description",
            "id": 1,
            "price": 99.99,
            "sale_price": 99.98,
            "stock": 123,
            "meta_description": "This is the updated meta description",
            "meta_key": "Color",
            "meta_value": "Purple Zebra"
        }))
        data = loads(req.data)

        self.assertIn('200 OK', req.status, 'Unable to update user\'s item.')

    def test_updateItemWithoutPermission(self):
        req = self.client.put('/api/v1/items/details.json', data=dumps({
            "jwt_token": None,
            "name": "Item1",
            "description": "This is the new description",
            "id": 1,
            "price": 99.99,
            "sale_price": 99.98,
            "stock": 123,
            "meta_description": "This is the updated meta description",
            "meta_key": "Color",
            "meta_value": "Yellow Zebra"
        }))
        self.assertIn('401 UNAUTHORIZED', req.status,
                      'Updating an item without permission returns %s instead of 401 UNAUTHORIZED.' % req.status)

        req = self.client.get('/api/v1/items/details.json?name=Item1')
        data = loads(req.data)
        itemMeta = data.get('item_meta')
        for im in itemMeta:
            if im.get('id') == 1:
                self.assertEqual(im.get('meta_value'), 'Purple', 'Item Meta was updated without permission.')
