from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from app.resources.DomainResource import *
from app.resources.ProposalResource import *
from app.resources.BackersResource import *
from app.resources.VoteResource import *
from app.resources.LoginResource import *
from app.resources.DemoResource import *

def main():
    app = webapp.WSGIApplication(
        [
            ('/api/domains', DomainResource),
            ('/api/proposals', ProposalResource),
            ('/api/backers', BackersResource),
            ('/api/votes', VoteResource),
            ('/api/login', LoginResource),
            ('/api/demo', DemoResource)
        ],
        debug=True)

    run_wsgi_app(app)

if __name__ == "__main__":
    main()