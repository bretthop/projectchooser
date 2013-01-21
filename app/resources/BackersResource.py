from google.appengine.api import users
from google.appengine.ext import webapp

from app.data.beans import *

from app.util.JsonUtil import JsonUtil

class BackersResource(webapp.RequestHandler):
    def get(self):
        currentBacker = BackerBean()
        currentBacker.userId           = users.get_current_user().email()
        currentBacker.remaining_gold   = 1  #TODO: get actual value from model
        currentBacker.remaining_silver = 1  #TODO: get actual value from model
        currentBacker.remaining_bronze = 1  #TODO: get actual value from model

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(JsonUtil.simpleEncodeObject(currentBacker))

