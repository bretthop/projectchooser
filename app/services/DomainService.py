from app.data.model.Domain import Domain
from app.services.AuditService import AuditService

class DomainService:

    _auditService = AuditService()

    def createDomain(self, domain):
        """
        :type domain: Domain
        """
        domain.put()

        self._auditService.Audit("%s domain created" % domain.title, domain_id=domain.key().id())

        return domain

    def updateDomain(self, domainId, domainTitle, domainDescription, domainStatus):
        _domain = Domain.get_by_id(domainId)

        if domainTitle is not None:
            _domain.title = domainTitle

        if domainDescription is not None:
            _domain.description = domainDescription

        if domainStatus is not None:
            _domain.status = domainStatus

        Domain.save(_domain)

    def GetDomainsByStatus(self, domainStatus):
        result = Domain.gql("WHERE status = '" + domainStatus +"'")
        return result
