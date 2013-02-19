from google.appengine.ext import webapp
from app.resources.AuditService import AuditResource
from app.resources.BackerResource import BackerResource
from app.resources.BackerVoteResource import BackerVoteResource
from app.resources.DemoResources import *

from app.resources.DomainResource import *
from app.resources.ProposalResource import *
from app.resources.VoteResource import *
from app.resources.LoginResource import *

apiDispatcher = webapp.WSGIApplication(
    [
        ('/api/domains', DomainResource),
        ('/api/proposals', ProposalResource),
        ('/api/votes', VoteResource),
        ('/api/backers', BackerResource),
        ('/api/backerVotes', BackerVoteResource),
        ('/api/login', LoginResource),
        ('/api/audits', AuditResource),
        ('/api/demo/domain', DomainDemoResource),
        ('/api/demo/proposal', ProposalDemoResource),
        ('/api/demo/currentUser', CurrentUserDemoResource)
    ],
    debug=True)