from google.appengine.ext import webapp
from admin.AdminController import AdminController

adminDispatcher = webapp.WSGIApplication(
    [
        ('/doAdminAction', AdminController)
    ],
    debug=True)