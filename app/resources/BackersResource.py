from google.appengine.ext import webapp
from app.decorator.ProduceJson import *

from app.services.BackerService import *

class BackersResource(webapp.RequestHandler):
    _backerService = BackerService()

    @JsonSingleResult
    def get(self):
        return self._backerService.GetCurrentBackerBean()
