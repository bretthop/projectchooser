from google.appengine.ext import webapp

from app.data.models import *

class WithdrawResource(webapp.RequestHandler):
    def post(self):
        voteId = int(self.request.get('voteId'))

        if voteId:
            vote = Vote.get_by_id(voteId)

            #TODO: give vote (weight) back to Backer (to be able to use it again)

            if vote:
                vote.delete()

        self.redirect('/')
