from google.appengine.ext import webapp

from app.data.models import *
from app.services.ProposalService import *
from app.resources.RestApiResponse import RestApiResponse

from app.decorator.ProduceJson import *

class DemoResource(webapp.RequestHandler):

    _proposalService = ProposalService()

#    @JsonListResult
    @JsonSingleResult
    def get(self):
        domainId = self.request.get('domainId')
        results = self._proposalService.GetProposalsByDomainAndStatus(domainId, 'OPEN')

        result = RestApiResponse.init('200', results)

        return result