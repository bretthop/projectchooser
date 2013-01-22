from google.appengine.ext import db
from google.appengine.ext import webapp

from app.data.beans import *
from app.data.models import * # Must import every model we want to use in a GQL Statement

from app.services.ProposalService import *

from app.util.JsonUtil import JsonUtil

class ProposalResource(webapp.RequestHandler):

    _proposalService = ProposalService()

    def get(self):
        proposalBeans = self._proposalService.GetProposalBeansByStatus('OPEN')

        proposalBeans = sorted(proposalBeans, ProposalBean.compareTo)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(JsonUtil.simpleEncodeList(proposalBeans))

    def post(self):
        # TODO: Refactor this to be fully REST (the client should POST a vote object in the request body that we simply save
        propName = self.request.get('name')
        propDesc = self.request.get('description')
        if propName != '' and propDesc != '':
            proposal = self._proposalService.ProposalFactory(propName, propDesc, self.request.get('technologiesUsed'))
            proposal.put()
