from twisted.web.server import Site
from .root import RootResource
from .auth import AuthResource

root_resource = RootResource()
auth_resource = AuthResource()
root_resource.putChild('auth', auth_resource)

app_site = Site(root_resource)
