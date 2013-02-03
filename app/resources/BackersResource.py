from google.appengine.ext import webapp
from app.decorator.ProduceJson import *
from app.decorator.Secure import Secured

from app.services.BackerService import *

class BackersResource(webapp.RequestHandler):
    _backerService = BackerService()

    @Secured
    @JsonSingleResult
    def get(self):
        email = self.currentUser['email']

        return self._backerService.GetBackerByEmail(email)
