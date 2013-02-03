from google.appengine.ext import webapp
from app.services.BackerService import BackerService

class LoginResource(webapp.RequestHandler):
    _backerService = BackerService()

    def post(self):
        email    = self.request.get('email')
        password = self.request.get('password')

        user = self._backerService.VerifyBacker(email, password)

        if not user:
            self.response.set_status(400)