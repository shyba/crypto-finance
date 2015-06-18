from twisted.trial.unittest import TestCase
from mock import Mock
from twisted.web.test.test_web import DummyRequest
from twisted.web.http import OK, NOT_FOUND

from cryptosync.resources import make_site


def make_request(uri='', method='GET', args={}):
    site = make_site(authenticator=Mock())
    request = DummyRequest(uri.split('/'))
    request.method = method
    request.args = args
    resource = site.getResourceFor(request)
    request.render(resource)
    request.data = "".join(request.written)
    return request


class RootResourceResponseCodesTestCase(TestCase):

    def test_root_resource_ok(self):
        request = make_request()

        self.assertEquals(request.responseCode, OK)

    def test_root_resource_not_found_url(self):
        request = make_request(uri='shouldneverfindthisthing')

        self.assertEquals(request.responseCode, NOT_FOUND)


class AuthResourceTestCase(TestCase):

    def _try_auth(self, credentials, expected):
        request = make_request(uri='/auth/', method='POST', args=credentials)

        self.assertEquals(request.responseCode, OK)
        self.assertEquals(request.data, expected)

    def test_auth_success_with_good_parameters(self):
        credentials = {'username': 'myself', 'password': 'somethingawesome'}
        self._try_auth(credentials, '{"status": "success"}')

    def test_auth_failure_with_missing_parameters(self):
        credentials = {'username': 'myself', 'password': 'somethingawesome'}
        for (k, v) in credentials.items():
            self._try_auth({k: v}, '{"status": "failure"}')
