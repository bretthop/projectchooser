from app.data.models import *
from app.data.model.Domain import Domain

class ProposalService:

    def saveProposal(self, proposal):
        proposal.put()
        return proposal

    def GetProposalsByDomainAndStatus(self, domainId, status):
        result = db.Model()
        try:
            domain = Domain.get_by_id(int(domainId))
            result = Proposal.gql("WHERE status = '" + status +"' AND domain=:pDomain", pDomain=domain)
        except Exception as e:
            exception = e

        return result

    def GetProposalById(self, proposalId):
        return Proposal.get_by_id(int(proposalId))
