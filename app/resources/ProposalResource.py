from google.appengine.ext import webapp

from app.data.models import *
from app.decorator.ProduceJson import *
from app.services.BackerService import BackerService
from app.services.ProposalService import *
from app.util.JsonUtil import JsonUtil

class ProposalResource(webapp.RequestHandler):

    _proposalService = ProposalService()
    _backerService = BackerService()

    @JsonListResult
    def get(self):
        domainId = self.request.get('domainId')
        result = self._proposalService.GetProposalsByDomainAndStatus(domainId, 'OPEN')
        return result

    def post(self):
        proposal = JsonUtil.decodeToModel(self.request.body, Proposal)

        # TODO Get the backer from the JSON request. The client should send up the backer with the request.
        owner = self._backerService.GetCurrentBacker()

        proposal.owner = owner

        if proposal.name != '' and proposal.description != '':
            self._proposalService.saveProposal(proposal)