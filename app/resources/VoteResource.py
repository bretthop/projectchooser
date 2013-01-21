from google.appengine.ext import webapp

from app.services.VoteService import *

class VoteResource(webapp.RequestHandler):

    _voteService = VoteService()

    def post(self):
        # TODO: Refactor this to be fully REST (the client should POST a vote object in the request body that we simply save
        proposalId   = int(self.request.get('proposalId'))
        votingWeight = self.request.get('weight')

        self._voteService.VoteForProposal(proposalId, votingWeight)

    def delete(self):
        # TODO: Refactor this into having the 'voteId' as part of the URL (not as a param)
        voteId = int(self.request.get('voteId'))

        self._voteService.WithdrawVote(voteId)
