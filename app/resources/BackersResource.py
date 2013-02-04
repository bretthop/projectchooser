from google.appengine.ext import webapp
from app.data.enums.PermissionNameEnum import PermissionNameEnum
from app.decorator.ProduceJson import *
from app.decorator.Secure import Secured

from app.services.BackerService import *

class BackersResource(webapp.RequestHandler):
    _backerService = BackerService()

    @Secured([PermissionNameEnum.AVAILABLE_ALL])
    @JsonSingleResult
    def get(self):
        email = self.currentUser.email

        return self._backerService.GetBackerByEmail(email)
