from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp

from app.data.beans import *
from app.data.models import * # Must import every model we want to use in a GQL Statement

from app.util.JsonUtil import JsonUtil

# TODO: This will replace 'ProposalResource', this has been committed like this for testing and because it turned out to be to lengthy to replace everything at once
class APIProposalResource(webapp.RequestHandler):
    def get(self):
        proposals = db.GqlQuery('SELECT * FROM Proposal')
        proposalBeans = []

        for proposal in proposals:
            propBean = ProposalBean.fromEntity(proposal)

            proposalVotes = db.GqlQuery('SELECT * FROM Vote WHERE proposalId = {proposalId}'
            .format(proposalId = proposal.key().id()))

            propBean.setVotes(proposalVotes, users.get_current_user())

            proposalBeans.append(propBean)

        proposalBeans = sorted(proposalBeans, ProposalBean.compareTo)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(JsonUtil.jsonEncodeList(proposalBeans))

