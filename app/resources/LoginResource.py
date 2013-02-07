from google.appengine.ext import webapp
from app.decorator.ProduceJson import JsonSingleResult
from app.resources.RestApiResponse import RestApiResponse
from app.services.BackerService import BackerService
from app.util.HttpUtil import getAuthInfoFromHeader

class LoginResource(webapp.RequestHandler):
    _backerService = BackerService()

    @JsonSingleResult
    def post(self):
        authInfo = getAuthInfoFromHeader(self.request)

        user = self._backerService.VerifyBacker(authInfo['username'], authInfo['password'])

        if user:
            return RestApiResponse.init('200', user)
        else:
            self.response.set_status(400)
            return RestApiResponse.init('400')