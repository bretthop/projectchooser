from app.data.beans import *
from app.data.models import Backer

class BackerService:

    def GetCurrentBackerBean(self):
        currentBacker = BackerBean()
        currentBacker.userId           = users.get_current_user().email()
        currentBacker.remaining_gold   = 1  #TODO: get actual value from model
        currentBacker.remaining_silver = 1  #TODO: get actual value from model
        currentBacker.remaining_bronze = 1  #TODO: get actual value from model

        #currentBacker = self.BackerFactory(users.get_current_user().email())

        return currentBacker

    def BackerFactory(self, email):
        result = Backer()

        result.userId = email
        result.remaining_gold = 1
        result.remaining_silver = 1
        result.remaining_bronze = 1

        return result
