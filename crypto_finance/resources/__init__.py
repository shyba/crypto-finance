from twisted.web.server import Site
from .root import RootResource
from .auth import AuthResource


def make_site(**kwargs):
    root_resource = RootResource()
    auth_resource = AuthResource(kwargs['authenticator'])
    root_resource.putChild('auth', auth_resource)

    return Site(root_resource)
