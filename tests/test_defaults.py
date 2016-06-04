from base import StoreAppTestCase
from json import dumps


class TestDefault(StoreAppTestCase):

    def setUp(self):
        super(TestDefault, self).setUp()

    def test_notFound(self):
        req = self.client.get('/urldoesnotexist')
        self.assertIn('404', req.status, 'Page not found error was not returned for page not found.')

    def test_methodNotSupported(self):
        req = self.client.get('/goauth')
        self.assertIn('405', req.status, 'Methods allowed for the endpoint are not being enforced.')

    def test_unauthorizedRequest(self):
        req = self.client.post('/reauth', content_type=self.ctype, data=dumps({
            'jwt_token': ''
        }))
        self.assertIn('401', req.status, 'Authorization before accessing endpoint is not required.')
