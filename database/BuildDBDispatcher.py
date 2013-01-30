from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from database.BuildDb import *

def main():
    app = webapp.WSGIApplication(
        [
            ('/database', BuildDb)
        ],
        debug=True)

    run_wsgi_app(app)

if __name__ == "__main__":
    main()