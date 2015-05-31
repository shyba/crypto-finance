from twisted.web.resource import Resource
from json import dumps


class AuthResource(Resource):
    isLeaf = True

    def __init__(self, authenticator):
        self.authenticator = authenticator

    def render_POST(self, request):
        request.setResponseCode(200)
        return dumps(self._auth(request.args))

    def _auth(self, args):
        has_user = len(args.get('username', '')) > 5
        has_pass = len(args.get('password', '')) > 5
        nothing_more = len(args.keys()) == 2
        if has_user and has_pass and nothing_more:
            self.authenticator(args.values())
            return {'status': 'success'}
        else:
            return {'status': 'failure'}
