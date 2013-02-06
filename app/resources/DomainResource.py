from google.appengine.ext import webapp
from app.data.enums.PermissionNameEnum import PermissionNameEnum

from app.decorator.ProduceJson import *
from app.decorator.Secure import Secured
from app.services.BackerService import BackerService
from app.services.DomainService import DomainService
from app.data.model.Domain import Domain

class DomainResource(webapp.RequestHandler):

    _domainService = DomainService()
    _backerService = BackerService()

    @Secured([PermissionNameEnum.CAN_VIEW_DOMAIN])
    @JsonListResult
    def get(self):
        return self._domainService.GetDomainsByStatus('OPEN')

    @Secured([PermissionNameEnum.CAN_CREATE_DOMAIN])
    def post(self):
        domain = Pson.basicDecodeToModel(self.request.body, Domain)

        # TODO Get the backer from the JSON request. The client should send up the backer with the request.
        #owner = self._backerService.GetCurrentBacker()
        #domain.owner = owner

        if domain.title != '' and domain.description != '':
            self._domainService.createDomain(domain)