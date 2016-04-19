import unittest
from store_app import create_app
from store_app.extensions import db
from store_app.config import TestingConfig
from store_app.database import User, Item, Category
from store_app import dummy_data


class StoreAppTestCase(unittest.TestCase):

    ctype = 'application/json'

    def setUp(self):
        self.app = create_app('Test App', config=TestingConfig)
        self.client = self.app.test_client(use_cookies=False)
        self.ctx = self.app.test_request_context()
        self.ctx.push()
        self.init_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all(app=self.app)
        self.ctx.pop()

    def init_data(self):
        db.drop_all(app=self.app)
        db.init_app(app=self.app)
        db.create_all(app=self.app)
        dummy_data.create_test_data(self.app)
