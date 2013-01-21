from google.appengine.ext import webapp

from app.services.BackerService import *

from app.util.JsonUtil import JsonUtil

class BackersResource(webapp.RequestHandler):
    _backerService = BackerService()

    def get(self):
        currentBacker = self._backerService.GetCurrentBackerBean()

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(JsonUtil.simpleEncodeObject(currentBacker))