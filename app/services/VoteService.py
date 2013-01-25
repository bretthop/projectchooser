from google.appengine.api import users

from app.data.models import *
#from app.util.EnumUtil import enum

class VoteService:

    #_voteTypeEnum = enum('GOLD', 'SILVER', 'BRONZE')

    def VoteForProposal(self, proposalId, votingWeight):

        # get the vote type
        _voteType = VoteService.GetVoteTypeByLabel(str(votingWeight).upper())

        #TODO: validate if backer still has enough remaining votes of _voteType

        # get the proposal user is voting for
        _proposal = Proposal.get_by_id(proposalId)

        # save the vote for the proposal (with user)
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

    @staticmethod
    def GetVoteTypeByLabel(label):
        _voteTypeId = db.GqlQuery("SELECT __key__ FROM VoteType WHERE label = '" + label + "'").get().id()
        result = VoteType.get_by_id(_voteTypeId)

        return result