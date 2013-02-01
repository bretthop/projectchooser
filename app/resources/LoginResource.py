from google.appengine.ext import webapp

import app.stormpath.Stormpath as storm

class LoginResource(webapp.RequestHandler):
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        # Example user and pass:
        # username = 'test@example.com'
        # password = 'Passwod1'

        loginResult = storm.login(username, password)

        if not loginResult:
            self.response.set_status(400)
