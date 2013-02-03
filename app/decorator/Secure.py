from app.stormpath.httpUtils import *
import app.stormpath.Stormpath as storm

def Secured(func):
    def secure(self):
        authorisation = self.request.headers["Authorization"]

        authInfo = decodeAuth(authorisation.split('Basic ')[1])
        username = authInfo['username']
        password = authInfo['password']

        # ATM, 'login' will only return an object that contains a HREF to the actual user account
        # TODO: Get login to return the full user object from Stormpath and remove manual addition of username
        currentUser = storm.login(username, password)

        if currentUser:
            # Complete above TO-DO and remove this
            currentUser['email'] = username

            self.currentUser = currentUser
            func(self)
        else:
            self.response.set_status(401)

    return secure