from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from app.data.models import *
from app.data.beans import *

# Handlers
# TODO: Move to separate files
class ProposalsHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()

        currentBacker = BackerBean()
        currentBacker.userId           = user.email()
        currentBacker.remaining_gold   = 0
        currentBacker.remaining_silver = 1
        currentBacker.remaining_bronze = 1

        proposalBeans = []
        proposals = db.GqlQuery('SELECT * FROM Proposal')

        for proposal in proposals:
            propBean = ProposalBean.fromEntity(proposal)

            userVote = db.GqlQuery('SELECT * FROM Vote WHERE userId = \'{userId}\' AND proposalId = {proposalId}'
                .format(userId = user.email(), proposalId = proposal.key().id()))

            if userVote.count() > 0:
                proposalVotes = db.GqlQuery('SELECT * FROM Vote WHERE proposalId = {proposalId}'
                    .format(proposalId = proposal.key().id()))
                propBean.setVotes(proposalVotes)

                propBean.hasUserVoted = True

            proposalBeans.append(propBean)

        data = { 'proposals': sorted(proposalBeans, ProposalBean.compare), 'currentBacker': currentBacker }
        self.response.out.write(template.render('templates/proposals.html', data))

    def post(self):
        proposal = Proposal(
            name = self.request.get('name'),
            description = self.request.get('description'),
            technologiesUsed = self.request.get('technologiesUsed'),
            rating = 0
        )

        proposal.put()

        self.redirect('/')

class VoteHandler(webapp.RequestHandler):
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

def main():
    app = webapp.WSGIApplication(
        [('/', ProposalsHandler),
         ('/vote', VoteHandler)],
        debug=True)

    run_wsgi_app(app)

if __name__ == "__main__":
    main()