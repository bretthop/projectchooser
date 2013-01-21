from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from app.resources.ProposalResource import *
from app.resources.BackersResource import *
from app.resources.VoteResource import *

def main():
    app = webapp.WSGIApplication(
        [
            ('/api/proposals', ProposalResource),
            ('/api/backers', BackersResource),
            ('/api/votes', VoteResource)
        ],
        debug=True)

    run_wsgi_app(app)

if __name__ == "__main__":
    main()