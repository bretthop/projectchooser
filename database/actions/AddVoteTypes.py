from google.appengine.ext import webapp

from app.services.VoteService import *

class AddVoteTypes(webapp.RequestHandler):

    _voteService = VoteService()

    def get(self):
        try:
            self._voteService.PopulateVoteTypes()

            self.response.out.write('Done!')
        except BaseException:
            self.response.out.write('Failed!')
