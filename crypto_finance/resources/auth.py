from twisted.web.resource import Resource


class AuthResource(Resource):
    isLeaf = True

    def render_POST(self, request):
        if not self._check_params(request.args):
            request.setResponseCode(404)
        else:
            # call leap.auth and keep credentials
            request.setResponseCode(200)

        return ""

    def _check_params(self, args):
        has_user = len(args.get('username', '')) > 5
        has_pass = len(args.get('password', '')) > 5
        nothing_more = len(args.keys()) == 2
        return has_user and has_pass and nothing_more
