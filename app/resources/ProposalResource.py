from google.appengine.ext import db
from google.appengine.ext import webapp

from app.data.models import * # Must import every model we want to use in a GQL Statement
from app.decorator.ProduceJson import *

from app.services.ProposalService import *

from app.util.JsonUtil import JsonUtil

class ProposalResource(webapp.RequestHandler):

    _proposalService = ProposalService()

    @JsonListResult
    def get(self):
        return self._proposalService.GetProposalsByStatus('OPEN')

    def post(self):
        proposalJson = JsonUtil.decodeToDict(self.request.body)
        proposal = Proposal.fromJson(proposalJson)

        if proposal.name != '' and proposal.description != '':
            self._proposalService.saveProposal(proposal)
