from base import StoreAppTestCase
from json import loads


class TestItem(StoreAppTestCase):

    def test_itemEndpointExists(self):
        self.endpointExists('/item')
