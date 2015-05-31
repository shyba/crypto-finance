from leap.auth import SRPAuth


def authenticate(user, password, cert_file, api):
    srp_auth = SRPAuth(api, cert_file)
    auth = srp_auth.authenticate(user, password)
    return auth.__dict__.copy()
