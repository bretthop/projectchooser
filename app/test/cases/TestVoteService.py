from app.test.cases.BaseUnitTest import BaseUnitTest

from google.appengine.ext import db

from app.data.models import Proposal
from app.data.enums.VoteTypeEnum import VoteTypeEnum

from app.services.ProposalService import ProposalService
from app.services.VoteService import VoteService

class TestVoteService(BaseUnitTest):

    _voteService = None
    _testProposalName = 'TEST PROPOSAL #1'
    _backerEmail = 'test_backer_2013-01-29@project.chooser.com.au'

#    addExpectedFailure = None

    #singleton pattern
    def getProposalService(self):
        if self._proposalService is None:
            self._proposalService = ProposalService()

        return self._proposalService

    #singleton pattern
    def getVoteService(self):
        if self._voteService is None:
            self._voteService = VoteService()

        return self._voteService

    def test_voteForProposal(self):
        _proposalId = db.GqlQuery("SELECT __key__ FROM Proposal WHERE name = '" + self._testProposalName + "'").get().id()
        _voteTypeLabel = VoteTypeEnum.GOLD

        self.getVoteService().VoteForProposal(_proposalId, _voteTypeLabel, self._backerEmail)

        self.reportResult(message='voted')

        _proposal = Proposal.get_by_id(_proposalId)

        self.assertIsNotNone(_proposal, 'Proposal is None')
        self.assertTrue(_proposal.votes.count() > 0, 'Proposal has no votes')

        if _proposal is not None and _proposal.votes.count() > 0:
            for v in _proposal.votes:
                if v.voteType.label == VoteTypeEnum.GOLD:
                    self.reportResult(message='vote saved successfully')
