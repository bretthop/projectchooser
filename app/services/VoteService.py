from google.appengine.api import users

from app.data.models import *

class VoteService:

    def VoteForProposal(self, proposalId, votingWeight):
        votingWeightInt = 0

        # TODO: Make this an enum or a model
        if votingWeight == 'gold':
            votingWeightInt = 8
        elif votingWeight == 'silver':
            votingWeightInt = 5
        elif votingWeight == 'bronze':
            votingWeightInt = 3

        # Apply vote to proposal
        proposal = Proposal.get_by_id(proposalId)
        proposal.put()

        # Record the vote for the user
        user = users.get_current_user()
        Vote(
            userId = user.nickname(),
            proposalId = proposalId,
            weight = votingWeightInt
        ).put()

    def WithdrawVote(self, voteId):
        if voteId:
            vote = Vote.get_by_id(voteId)

            #TODO: give vote (weight) back to Backer (to be able to use it again)

            if vote:
                vote.delete()
                return True

        return False