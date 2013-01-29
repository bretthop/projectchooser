from app.data.models import *

class ProposalService:

    def saveProposal(self, proposal):
        proposal.put()
        return proposal

    def GetProposalsByStatus(self, status):
        return Proposal.gql("WHERE status = '" + status +"'")
