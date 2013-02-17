import webapp2
import proposal_votes
from google.appengine.ext import deferred

class StabilizeDatastoreHandler(webapp2.RequestHandler):
    def get(self):
        deferred.defer(proposal_votes.AddBackerToProposalVotes)
        self.response.out.write('<div>Datastore fix "AddBackerToProposalVotes" successfully initiated.</div>')

        deferred.defer(proposal_votes.RemoveVoteUserId)
        self.response.out.write('<div>Datastore fix "AddBackerToProposalVotes" successfully initiated.</div>')

app = webapp2.WSGIApplication([('/fix_datastore', StabilizeDatastoreHandler)])


