from google.appengine.ext import webapp
from app.decorator.ProduceJson import ProduceJson

from app.resources.RestApiResponse import RestApiResponse
from app.services.AuditService import AuditService

class AuditResource(webapp.RequestHandler):

    _auditService = AuditService()

    @ProduceJson
    def get(self):
        audits = self._auditService.GetAll()

        return RestApiResponse.init('200', audits)