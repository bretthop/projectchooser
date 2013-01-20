from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from app.resources.APIProposalResource import *

def main():
    app = webapp.WSGIApplication(
        [
            ('/api/proposals', APIProposalResource)
        ],
        debug=True)

    run_wsgi_app(app)

if __name__ == "__main__":
    main()