from google.appengine.ext import webapp
from app.data.factory.JsonFactory import *
from app.decorator.ProduceJson import ProduceJson

from app.resources.RestApiResponse import RestApiResponse
from app.services.BackerService import BackerService

class BackerResource(webapp.RequestHandler):

    _backerService = BackerService()

    @ProduceJson
    def post(self):
        backer = toBacker(self.request.body)

        backer = self._backerService.CreateBacker(backer.email, backer.username, backer.password, backer.role)

        return RestApiResponse.init('200', backer)