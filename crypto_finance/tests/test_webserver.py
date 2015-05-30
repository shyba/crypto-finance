from twisted.trial.unittest import TestCase
from twisted.web.test.test_web import DummyRequest
from twisted.web.test._util import _render
from twisted.web.http import OK, NOT_FOUND

from crypto_finance.resources.root import CryptoFinanceRootResource


class RootResourceResponseCodesTestCase(TestCase):

    def test_root_resource_ok(self):
        request = DummyRequest([''])
        request.method = 'GET'
        resource = CryptoFinanceRootResource().getChild('', request)
        d = _render(resource, request)

        def _check(_):
            self.assertEquals(request.responseCode, OK)
        d.addCallback(_check)
        return d

    def test_root_resource_not_found_url(self):
        request = DummyRequest([''])
        request.method = 'GET'
        resource = CryptoFinanceRootResource(
            ).getChild('shouldnotfind', request)
        d = _render(resource, request)

        def _check(_):
            self.assertEquals(request.responseCode, NOT_FOUND)
        d.addCallback(_check)
        return d
