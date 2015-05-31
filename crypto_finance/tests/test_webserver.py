from twisted.trial.unittest import TestCase
from twisted.web.test.test_web import DummyRequest
from twisted.web.http import OK, NOT_FOUND

from crypto_finance.resources import app_site


def make_request(uri='', method='GET', args={}):
    request = DummyRequest(uri.split('/'))
    request.method = method
    request.args = args
    resource = app_site.getResourceFor(request)
    request.render(resource)
    return request


class RootResourceResponseCodesTestCase(TestCase):

    def test_root_resource_ok(self):
        request = make_request()

        self.assertEquals(request.responseCode, OK)

    def test_root_resource_not_found_url(self):
        request = make_request(uri='shouldneverfindthisthing')

        self.assertEquals(request.responseCode, NOT_FOUND)


class AuthResourceTestCase(TestCase):

    def test_auth_resource_ok_with_good_parameters(self):
        args = {'username': 'myself', 'password': 'somethingawesome'}
        request = make_request(uri='/auth/', method='POST', args=args)

        self.assertEquals(request.responseCode, OK)
