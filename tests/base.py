import unittest
from store_app import create_app
from store_app.extensions import db
from store_app.config import TestingConfig
from store_app.database import User, Item, Category


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
        for i in range(10):
            newUser = User(
                username='Tester%s' % str(i),
                email='Tester%s@email.com' % str(i),
                password='lol123'
            )
            db.session.add(newUser)
        db.session.commit()
        for i in range(10):
            newItem = Item(
                name='TestItem%s' % str(i),
                description='This is TestItem%s' % str(i),
                price=10.50,
                sale_price=10.50,
                stock=10
            )
            db.session.add(newItem)
        db.session.commit()
        for i in range(5):
            newCat = Category(
                name='TestCategory%s' % str(i)
            )

    def assert_status(self, status, response, msg):
        message = msg or 'Expected status %s but received status %s.' % (status, response.status)
        self.assertEqual(status, response.status, message)

    def endpointExists(self, ep):
        req = self.client.get(ep)
        self.assert_status('200 OK', req, 'Endpoint \'%s\' does not exist.' % ep)
