from google.appengine.ext import webapp
from app.data.enums.PermissionNameEnum import PermissionNameEnum

from app.decorator.Secure import Secured
from app.services.BackerService import BackerService
from app.services.ProposalService import *
from app.resources.RestApiResponse import RestApiResponse

from app.decorator.ProduceJson import ProduceJson

class DomainDemoResource(webapp.RequestHandler):

    _proposalService = ProposalService()

    @ProduceJson
    def get(self):
        domainId = self.request.get('domainId')
        results = self._proposalService.GetProposalsByDomainAndStatus(domainId, 'OPEN')

        result = RestApiResponse.init('200', results)

        return result

class ProposalDemoResource(webapp.RequestHandler):

    _proposalService = ProposalService()

    @Secured([PermissionNameEnum.AVAILABLE_ALL])
    @ProduceJson
    def get(self):
        proposalId = self.request.get('proposalId')
        results = self._proposalService.GetProposalById(proposalId)

        result = RestApiResponse.init('200', results)

        return result

class CurrentUserDemoResource(webapp.RequestHandler):

    _backerService = BackerService()

    @Secured([PermissionNameEnum.AVAILABLE_ALL])
    @ProduceJson
    def get(self):
        user = self.currentUser

        # Add some random properties to test db.Expando serialisation
        user.openProposals = ['test1', 'test2', 'test3']
        user.randomProp47  = 34533

        return RestApiResponse.init('200', user)
