from base import StoreAppTestCase
from json import loads


class TestCategory(StoreAppTestCase):

    def test_categoryEndpointExists(self):
        self.endpointExists('/category')
