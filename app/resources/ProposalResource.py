from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from app.data.beans import *
from app.data.models import *

class ProposalResource(webapp.RequestHandler):
    def get(self):
        currentUser = users.get_current_user()

        currentBacker = BackerBean()
        currentBacker.userId           = currentUser.email()
        currentBacker.remaining_gold   = 1  #TODO: get actual value from model
        currentBacker.remaining_silver = 1  #TODO: get actual value from model
        currentBacker.remaining_bronze = 1  #TODO: get actual value from model

        proposalBeans = []
        proposals = db.GqlQuery('SELECT * FROM Proposal')

        for proposal in proposals:
            propBean = ProposalBean.fromEntity(proposal)

            proposalVotes = db.GqlQuery('SELECT * FROM Vote WHERE proposalId = {proposalId}'
            .format(proposalId = proposal.key().id()))

            propBean.setVotes(proposalVotes, currentUser)

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