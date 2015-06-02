from twisted.trial.unittest import TestCase
from crypto_finance.sync import auth
from mock import patch
from mock import Mock


class AuthTestCase(TestCase):

    @patch('leap.auth.SRPAuth', autospec=True)
    def test_authorize_calls(self, fake_srp):
        auth.SRPAuth = fake_srp
        auth.authenticate('user', 'pass',
                          'ca.crt', 'api')
        fake_srp.assert_called_once_with('api', 'ca.crt')
        instance = fake_srp.return_value
        instance.authenticate.assert_called_once_with('user', 'pass')

    def test_configured_authenticator(self):
        auth.authenticate = Mock()
        authenticator = auth.configure_authenticator('ca.crt', 'api')

        authenticator('user', 'pass')

        auth.authenticate.assert_called_once_with('user', 'pass',
                                                  cert_file='ca.crt',
                                                  api='api')
