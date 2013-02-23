from google.appengine.ext import webapp
from app.data.enums.PermissionNameEnum import PermissionNameEnum
from app.decorator.ProduceJson import *
from app.decorator.Secure import Secured
from app.resources.RestApiResponse import RestApiResponse
from app.services.ProposalService import *

class ProposalWinningResource(webapp.RequestHandler):

    _proposalService = ProposalService()

    @Secured([PermissionNameEnum.CAN_VIEW_PROPOSAL])
    @ProduceJson
    def get(self):
        result = None
        proposals = self._proposalService.GetProposalsByStatus('OPEN')

        #filter out proposals that have no votes
        for p in proposals:
            if p.totalRating > 0:
                if result is None:
                    result = []

                result.append(p)

        if result:
            #sort all voted proposals by totalRating DESC
            result = sorted(result, key=lambda Proposal: Proposal.totalRating, reverse=True)

            #keep only the top 3 proposals
            result = result[0:3]

        return RestApiResponse.init('200', result)
