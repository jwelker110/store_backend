from base import StoreAppTestCase
from json import loads


class TestCategory(StoreAppTestCase):

    def setUp(self):
        super(TestCategory, self).setUp()
        # perform some other set up here

    def test_getCategories(self):
        req = self.client.get('/api/v1/categories.json')
        data = loads(req.data)
        cats = data.get('categories')
        self.assertEqual(5, len(cats), 'Did not retrieve 5 categories.')
