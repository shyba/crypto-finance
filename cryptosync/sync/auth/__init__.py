from leap.auth import SRPAuth
from functools import partial


def authenticate(user, password, cert_file, api):
    srp_auth = SRPAuth(api, cert_file)
    auth = srp_auth.authenticate(user, password)
    return auth.__dict__.copy()


def configure_authenticator(cert_file, api):
    return partial(authenticate, cert_file=cert_file, api=api)
