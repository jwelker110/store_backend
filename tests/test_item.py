from base import StoreAppTestCase
from json import loads, dumps


class TestItem(StoreAppTestCase):

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

    def test_getItemsByCategory(self):
        req = self.client.get('/api/v1/items.json?category=Category1')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(2, len(items), 'Expected 2 items in \'Category1\', retrieved %s.' % str(len(items)))

    def test_getItemsByCategoryOffset(self):
        req = self.client.get('/api/v1/items.json?category=Category1&offset=1')
        data = loads(req.data)
        items = data.get('items')
        self.assertEqual(1, len(items), 'Expected 1 item in \'Category1\' when offset by 1, retrieved %s' % str(len(items)))

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
        pass
