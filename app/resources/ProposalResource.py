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
        proposalJson = JsonUtil.decodeToDict(self.request.body)
        proposalBean = ProposalBean.fromJson(proposalJson)

        if proposalBean.name != '' and proposalBean.description != '':
            self._proposalService.saveProposal(proposalBean)
