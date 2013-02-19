from app.data.models import *

class AuditService:
    def Audit(self, message, domain=None, proposal=None, backer=None):
        Audit(
            message=message,
            domain=domain,
            proposal=proposal,
            backer=backer
        ).put()

    def GetAll(self):
        audits = Audit.all()

        audits = sorted(audits, Audit.dateDesc)

        return audits