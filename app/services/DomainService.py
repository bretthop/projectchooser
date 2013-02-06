from app.data.model.Domain import Domain

class DomainService:

    def createDomain(self, domain):
        """
        :type domain: Domain
        """
        domain.put()
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
