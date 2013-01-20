from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from app.data.beans import *
from app.data.models import *

class ProposalResource(webapp.RequestHandler):
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

            proposalVotes = db.GqlQuery('SELECT * FROM Vote WHERE proposalId = {proposalId}'
            .format(proposalId = proposal.key().id()))

            propBean.setVotes(proposalVotes)

            userVote = db.GqlQuery('SELECT * FROM Vote WHERE userId = \'{userId}\' AND proposalId = {proposalId}'
            .format(userId = user.email(), proposalId = proposal.key().id()))

            if userVote.count() > 0:
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