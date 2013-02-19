from app.data.models import *
from app.data.model.Domain import Domain
from app.services.AuditService import AuditService

class ProposalService:

    _auditService = AuditService()

    def saveProposal(self, proposal):
        proposal.put()

        self._auditService.Audit("%s proposal created (In %s domain)" % (proposal.name, proposal.domain.title),
            domain_id=proposal.domain.key().id(),
            proposal_id=proposal.key().id()
        )

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
