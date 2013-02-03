from app.services.BackerService import BackerService
from app.util.HttpUtil import decodeAuth

def Secured(func):
    def secure(self):
        _backerService = BackerService()

        authorisation = self.request.headers["Authorization"]

        authInfo = decodeAuth(authorisation.split('Basic ')[1])
        email = authInfo['username']
        password = authInfo['password']

        user = _backerService.VerifyBacker(email, password)

        if user:
            self.currentUser = user
            func(self)
        else:
            self.response.set_status(401)

    return secure