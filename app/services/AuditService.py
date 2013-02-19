from app.data.models import *

class AuditService:
    def Audit(self, message, domain_id=None, proposal_id=None, backer_id=None):
        audit = Audit(message=message)

        if domain_id:
            audit.domain = Domain.get_by_id(domain_id)

        if proposal_id:
            audit.proposal = Proposal.get_by_id(proposal_id)

        if backer_id:
            audit.backer = Backer.get_by_id(backer_id)

        audit.put()

    def GetAll(self):
        audits = Audit.all()

        audits = sorted(audits, Audit.dateDesc)

        return audits