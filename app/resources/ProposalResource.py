from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp

from app.data.beans import *
from app.data.models import * # Must import every model we want to use in a GQL Statement

from app.util.JsonUtil import JsonUtil

class ProposalResource(webapp.RequestHandler):
    def get(self):
        proposals = db.GqlQuery('SELECT * FROM Proposal')
        proposalBeans = []

        for proposal in proposals:
            propBean = ProposalBean.fromEntity(proposal)

            proposalVotes = db.GqlQuery('SELECT * FROM Vote WHERE proposalId = {proposalId}'
            .format(proposalId = proposal.key().id()))

            propBean.setVotes(VoteBean.fromEntities(proposalVotes), users.get_current_user())

            proposalBeans.append(propBean)

        proposalBeans = sorted(proposalBeans, ProposalBean.compareTo)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(JsonUtil.simpleEncodeList(proposalBeans))

    def post(self):
        # TODO: Refactor this to be fully REST (the client should POST a vote object in the request body that we simply save
        proposal = Proposal(
            name = self.request.get('name'),
            description = self.request.get('description'),
            technologiesUsed = self.request.get('technologiesUsed'),
            rating = 0
        )

        proposal.put()