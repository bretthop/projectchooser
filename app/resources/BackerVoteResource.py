from google.appengine.ext import webapp
from app.data.enums.PermissionNameEnum import PermissionNameEnum
from app.decorator.ProduceJson import JsonSingleResult
from app.decorator.Secure import Secured
from app.resources.RestApiResponse import RestApiResponse
from app.services.BackerVoteService import BackerVoteService

class BackerVoteResource(webapp.RequestHandler):

    _backerVoteService = BackerVoteService()

    @Secured([PermissionNameEnum.AVAILABLE_ALL])
    @JsonSingleResult
    def get(self):
        backerId = int(self.request.get('backerId'))

        result = self._backerVoteService.GetBackerVotesByBackerId(backerId)

        return RestApiResponse.init('200', result)