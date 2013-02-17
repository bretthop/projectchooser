from google.appengine.ext import webapp
from admin.datastore_updates.StabilizeDatastoreHandler import StabilizeDatastoreHandler

dbHandler = webapp.WSGIApplication(
    [
        ('/fix_datastore', StabilizeDatastoreHandler)
    ],
    debug=True)