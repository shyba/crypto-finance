from twisted.trial.unittest import TestCase
from crypto_finance.sync import auth
from mock import patch


class AuthTestCase(TestCase):

    @patch('leap.auth.SRPAuth', autospec=True)
    def test_authorize_calls(self, fake_srp):
        auth.SRPAuth = fake_srp
        auth.authenticate('user', 'pass',
                          'ca.crt', 'api')
        fake_srp.assert_called_once_with('api', 'ca.crt')
        instance = fake_srp.return_value
        instance.authenticate.assert_called_once_with('user', 'pass')
