from google.appengine.ext import webapp

from app.decorator.ProduceJson import *
from app.decorator.Secure import Secured
from app.services.BackerService import BackerService
from app.services.DomainService import DomainService
from app.util.JsonUtil import JsonUtil
from app.data.model.Domain import Domain
from app.data.models import *

class DomainResource(webapp.RequestHandler):

    _domainService = DomainService()
    _backerService = BackerService()

    @Secured
    @JsonListResult
    def get(self):
        return self._domainService.GetDomainsByStatus('OPEN')

    @Secured
    def post(self):
        domain = JsonUtil.decodeToModel(self.request.body, Domain)

        # TODO Get the backer from the JSON request. The client should send up the backer with the request.
        #owner = self._backerService.GetCurrentBacker()
        #domain.owner = owner

        if domain.title != '' and domain.description != '':
            self._domainService.createDomain(domain)