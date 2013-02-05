from google.appengine.ext import webapp
from app.data.enums.PermissionNameEnum import PermissionNameEnum
from app.data.factory.JsonFactory import toProposal

from app.data.models import *
from app.data.model.Domain import Domain
from app.decorator.ProduceJson import *
from app.decorator.Secure import Secured
from app.services.BackerService import BackerService
from app.services.ProposalService import *
from app.util.JsonUtil import JsonUtil

class ProposalResource(webapp.RequestHandler):

    _proposalService = ProposalService()
    _backerService = BackerService()

    @Secured([PermissionNameEnum.CAN_VIEW_PROPOSAL])
    @JsonListResult
    def get(self):
        domainId = self.request.get('domainId')
        result = self._proposalService.GetProposalsByDomainAndStatus(domainId, 'OPEN')
        return result

    @Secured([PermissionNameEnum.CAN_CREATE_PROPOSAL])
    def post(self):
        proposal = toProposal(self.request.body)

        # TODO Get the backer from the JSON request. The client should send up the backer with the request.
        _owner = self._backerService.GetBackerByEmail(self.currentUser.email)
        proposal.owner = _owner

        if proposal.name != '' and proposal.description != '':
            self._proposalService.saveProposal(proposal)