from google.appengine.ext import webapp

from app.data.models import *
from app.decorator.ProduceJson import *
from app.services.ProposalService import *
from app.util.JsonUtil import JsonUtil

class ProposalResource(webapp.RequestHandler):

    _proposalService = ProposalService()

    @JsonListResult
    def get(self):
        return self._proposalService.GetProposalsByStatus('OPEN')

    def post(self):
        proposal = JsonUtil.decodeToModel(self.request.body, Proposal)

        if proposal.name != '' and proposal.description != '':
            self._proposalService.saveProposal(proposal)