from app.data.beans import *

class BackerService:

    def GetCurrentBackerBean(self):
        currentBacker = BackerBean()
        currentBacker.userId           = users.get_current_user().email()
        currentBacker.remaining_gold   = 1  #TODO: get actual value from model
        currentBacker.remaining_silver = 1  #TODO: get actual value from model
        currentBacker.remaining_bronze = 1  #TODO: get actual value from model

        return currentBacker
