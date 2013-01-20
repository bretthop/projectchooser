from google.appengine.api import users
from google.appengine.ext import webapp

from app.data.models import *

class VoteResource(webapp.RequestHandler):
    def post(self):
        proposalId = int(self.request.get('id'))
        votingWeight = self.request.get('weight')
        votingWeightInt = 0

        # TODO: Make this an enum or a model
        if votingWeight == 'gold':
            votingWeightInt = 8
        elif votingWeight == 'silver':
            votingWeightInt = 5
        elif votingWeight == 'bronze':
            votingWeightInt = 3

        # Apply vote to proposal
        proposal = Proposal.get_by_id(proposalId)
        proposal.put()

        # Record the vote for the user
        user = users.get_current_user()
        Vote(
            userId = user.nickname(),
            proposalId = proposalId,
            weight = votingWeightInt
        ).put()

        self.redirect('/')