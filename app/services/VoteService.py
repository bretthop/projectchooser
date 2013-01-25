from google.appengine.api import users

from app.data.models import *
from app.services.BackerService import BackerService
from app.util.VoteTypeUtil import VoteTypeUtil

class VoteService:

    _backerService = BackerService()

    def VoteForProposal(self, proposalId, votingWeight):
        #get current user
        userEmail = users.get_current_user().email()

        # ensure label name is all in uppercase
        votingWeight = str(votingWeight).upper()

        # get the vote type by label
        _voteType = VoteTypeUtil.GetVoteTypeByLabel(votingWeight)

        #validate if backer still has enough remaining votes of _voteType
        if self._backerService.BackerHasVoteType(userEmail, _voteType):
            # get the proposal user is voting for
            _proposal = Proposal.get_by_id(proposalId)

            # save the vote for the proposal (with user)
            Vote(
                userId = userEmail,
                proposal = _proposal,
                voteType = _voteType
            ).put()

            #TODO: remove _voteType from BackerVote pool

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
#        vt.label = self._voteTypeEnum.GOLD
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
