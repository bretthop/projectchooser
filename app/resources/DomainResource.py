from google.appengine.ext import webapp
from app.data.enums.PermissionNameEnum import PermissionNameEnum

from app.decorator.ProduceJson import *
from app.decorator.Secure import Secured
from app.resources.RestApiResponse import RestApiResponse
from app.services.AuditService import AuditService
from app.services.BackerService import BackerService
from app.services.DomainService import DomainService
from app.data.model.Domain import Domain

class DomainResource(webapp.RequestHandler):

    _domainService = DomainService()
    _backerService = BackerService()
    _auditService  = AuditService()

    @Secured([PermissionNameEnum.CAN_VIEW_DOMAIN])
    @ProduceJson
    def get(self):
        result = self._domainService.GetDomainsByStatus('OPEN')

        return RestApiResponse.init('200', result)

    @Secured([PermissionNameEnum.CAN_CREATE_DOMAIN])
    def post(self):
        domain = Pson.basicDecodeToModel(self.request.body, Domain)

        # TODO Get the backer from the JSON request. The client should send up the backer with the request (maybe?).
        #owner = self._backerService.GetCurrentBacker()
        #domain.owner = owner

        if domain.title != '' and domain.description != '':
            self._domainService.createDomain(domain)

            self._auditService.AuditAddDomain(domain, self.currentUser)