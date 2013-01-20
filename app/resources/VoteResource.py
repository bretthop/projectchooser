from google.appengine.ext import webapp

from app.services import VoteService

class VoteResource(webapp.RequestHandler):

    _voteService = VoteService.VoteService()

    def post(self):
        proposalId   = int(self.request.get('proposalId'))
        votingWeight = self.request.get('weight')

        self._voteService.VoteForProposal(proposalId, votingWeight)

        self.redirect('/')