import functools
from app.data.enums.PermissionNameEnum import PermissionNameEnum
from app.services.BackerService import BackerService
from app.util.HttpUtil import *

class Secured(object):
    _backerService = BackerService()

    def __init__(self, permissionNames):
        self.permissionNames = permissionNames

    def __call__(self, fn):
        @functools.wraps(fn)
        def secure(handler):
            authInfo = getAuthInfoFromHeader(handler.request)

            user = self._backerService.VerifyBacker(authInfo['username'], authInfo['password'])

            if user:
                userPermissionNames = []

                for permission in user.role.permissions:
                    userPermissionNames.append(permission.name)

                for p in self.permissionNames:
                    if p == PermissionNameEnum.AVAILABLE_ALL or p in userPermissionNames:
                        # The user is verified
                        handler.currentUser = user
                        fn(handler)

                        return

            handler.response.set_status(401)
        return secure