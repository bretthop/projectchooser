from google.appengine.ext import webapp

from app.services import VoteService

class WithdrawResource(webapp.RequestHandler):

    _voteService = VoteService.VoteService()

    def post(self):
        voteId = int(self.request.get('voteId'))

        self._voteService.WithdrawVote(voteId)

        self.redirect('/')
