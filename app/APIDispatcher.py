from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from app.resources.BackerVoteResource import BackerVoteResource
from app.resources.DemoResources import DomainDemoResource, ProposalDemoResource

from app.resources.DomainResource import *
from app.resources.ProposalResource import *
from app.resources.VoteResource import *
from app.resources.LoginResource import *

def main():
    app = webapp.WSGIApplication(
        [
            ('/api/domains', DomainResource),
            ('/api/proposals', ProposalResource),
            ('/api/votes', VoteResource),
            ('/api/backerVotes', BackerVoteResource),
            ('/api/login', LoginResource),
            ('/api/demo/domain', DomainDemoResource),
            ('/api/demo/proposal', ProposalDemoResource)
        ],
        debug=True)

    run_wsgi_app(app)

if __name__ == "__main__":
    main()