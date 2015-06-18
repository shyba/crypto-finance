from twisted.web.resource import Resource


class RootResource(Resource):

    def getChild(self, path, request):
        if path == '':
            return self
        return Resource.getChild(self, path, request)

    def render(self, request):
        request.setResponseCode(200)
        return ""
