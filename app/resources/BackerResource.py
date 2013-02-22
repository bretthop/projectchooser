from google.appengine.ext import webapp
from app.data.enums.PermissionNameEnum import PermissionNameEnum
from app.decorator.Secure import Secured
from app.data.factory.JsonFactory import *
from app.decorator.ProduceJson import ProduceJson

from app.resources.RestApiResponse import RestApiResponse
from app.services.BackerService import BackerService

class BackerResource(webapp.RequestHandler):

    _backerService = BackerService()

    @Secured([PermissionNameEnum.AVAILABLE_ALL])
    @ProduceJson
    def get(self):
        backer = self._backerService.GetBackerByEmail(self.currentUser.email)

        return RestApiResponse.init('200', backer)

    @ProduceJson
    def post(self):
        backer = toBacker(self.request.body)

        try :
            backer = self._backerService.CreateBacker(backer.email, backer.username, backer.password, backer.role)
        except ValueError:
            self.response.set_status(409) # TODO: Add a Process Request decorator that can handle RestApiResponses and return proper HTTP status from them
            return RestApiResponse.init('409')

        return RestApiResponse.init('200', backer)