from google.appengine.api import users

from app.data.models import *

class ProposalService:

    def saveProposal(self, proposal):
        proposal.put()

    def GetProposalBeansByStatus(self, status):
        return Proposal.gql("WHERE status = '" + status +"'")
