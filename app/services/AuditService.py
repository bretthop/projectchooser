from app.data.models import *

class AuditService:
    ADD_DOMAIN_MESSAGE = '%s domain created'
    ADD_PROPOSAL_MESSAGE = '%s proposal created (In %s domain)'

    def Audit(self, message, domain=None, proposal=None, backer=None, dateCreated=None):
        Audit(
            message=message,
            domain=domain,
            proposal=proposal,
            backer=backer,
            dateCreated=dateCreated
        ).put()

    def AuditAddDomain(self, domain, backer=None):
        self.Audit(
            AuditService.ADD_DOMAIN_MESSAGE % domain.title,
            domain=domain,
            backer=backer,
            dateCreated=domain.created
        )

    def AuditAddProposal(self, proposal):
        self.Audit(
            AuditService.ADD_PROPOSAL_MESSAGE % (proposal.name, proposal.domain.title),
            domain=proposal.domain,
            proposal=proposal,
            backer=proposal.owner,
            dateCreated=proposal.created
        )

    def GetAll(self):
        audits = Audit.all()

        audits = sorted(audits, Audit.dateDesc)

        return audits