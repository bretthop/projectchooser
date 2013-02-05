from google.appengine.ext import webapp
from app.data.enums.PermissionNameEnum import PermissionNameEnum

from app.decorator.Secure import Secured
from app.services.ProposalService import *
from app.resources.RestApiResponse import RestApiResponse

from app.decorator.ProduceJson import *

class DomainDemoResource(webapp.RequestHandler):

    _proposalService = ProposalService()

    @JsonSingleResult
    def get(self):
        domainId = self.request.get('domainId')
        results = self._proposalService.GetProposalsByDomainAndStatus(domainId, 'OPEN')

        result = RestApiResponse.init('200', results)

        return result

class ProposalDemoResource(webapp.RequestHandler):

    _proposalService = ProposalService()

    @Secured([PermissionNameEnum.AVAILABLE_ALL])
    @JsonSingleResult
    def get(self):
        proposalId = self.request.get('proposalId')
        results = self._proposalService.GetProposalById(proposalId)

        result = RestApiResponse.init('200', results, self.currentUser)

        return result