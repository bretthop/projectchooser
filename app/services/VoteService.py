from google.appengine.api import users

from app.data.models import *

class VoteService:

    def VoteForProposal(self, proposalId, votingWeight):
        votingWeightInt = 0
        _voteType = None

        # TODO: Make this an enum or a model
        if votingWeight == 'gold':
            votingWeightInt = 8
        elif votingWeight == 'silver':
            votingWeightInt = 5
        elif votingWeight == 'bronze':
            votingWeightInt = 3

        #VoteType.gql("WHERE weight = 8").get()._entity.key().id()
        _voteTypeId = db.GqlQuery("SELECT __key__ FROM VoteType WHERE weight = " + str(votingWeightInt)).get().id()
        _voteType = VoteType.get_by_id(_voteTypeId)

        # Apply vote to proposal
        _proposal = Proposal.get_by_id(proposalId)

        # Record the vote for the user
        user = users.get_current_user()
        Vote(
            userId = user.email(),
            proposal = _proposal,
            voteType = _voteType
        ).put()

    def WithdrawVote(self, voteId):
        if voteId:
            vote = Vote.get_by_id(voteId)

            #TODO: give vote (weight) back to Backer (to be able to use it again)

            if vote:
                vote.delete()
                return True

        return False

    def PopulateVoteTypes(self):
        vt = VoteType()
        vt.label = 'GOLD'
        vt.weight = 8
        vt.put()

        vt = VoteType()
        vt.label = 'SILVER'
        vt.weight = 5
        vt.put()

        vt = VoteType()
        vt.label = 'BRONZE'
        vt.weight = 3
        vt.put()