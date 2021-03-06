#from google.appengine.api import users

from app.data.models import *
from app.services.BackerService import BackerService
from app.util.VoteTypeUtil import VoteTypeUtil
from app.data.enums.VoteTypeEnum import VoteTypeEnum

class VoteService:

    _backerService = BackerService()

    def VoteForProposal(self, proposalId, voteTypeLabel, userEmail):
        #validate if backer still has enough remaining votes of _voteType
        if self._backerService.BackerHasVoteType(userEmail, voteTypeLabel):
            # get the vote type by label
            _voteType = VoteTypeUtil.GetVoteTypeByLabel(voteTypeLabel)

            # get the proposal user is voting for
            _proposal = Proposal.get_by_id(proposalId)

            # save the vote for the proposal (with user)
            _backer = self._backerService.GetBackerByEmail(userEmail)
            Vote(
                backer = _backer,
                proposal = _proposal,
                voteType = _voteType
            ).put()

            #remove voteType from BackerVote pool
            self._backerService.RemoveBackerVote(userEmail, voteTypeLabel)


    def WithdrawVote(self, voteId, userEmail):
        if voteId:
            vote = Vote.get_by_id(voteId)

            if vote:
                voteTypeLabel = vote.voteType.label
                vote.delete()

                #add voteType to BackerVote pool
                self._backerService.AddBackerVote(userEmail, voteTypeLabel)

                return True

        return False

    #TODO: remove this code or move it to some other location
    def PopulateVoteTypes(self):
        vt = VoteType()
        vt.label = VoteTypeEnum.GOLD
        vt.weight = 8
        vt.put()

        vt = VoteType()
        vt.label = VoteTypeEnum.SILVER
        vt.weight = 5
        vt.put()

        vt = VoteType()
        vt.label = VoteTypeEnum.BRONZE
        vt.weight = 3
        vt.put()
