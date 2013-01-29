from app.test.cases.BaseUnitTest import BaseUnitTest

from google.appengine.ext import db

from app.data.models import Proposal
from app.test.fixtures.TestVoteTypeEnum import TestVoteTypeEnum

from app.services.ProposalService import ProposalService
from app.services.VoteService import VoteService

class TestVoteService(BaseUnitTest):

    _voteService = None
    _testProposalName = 'TEST PROPOSAL #1'
    _backerEmail = 'test_backer_2013-01-29@project.chooser.com.au'

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
        _voteTypeLabel = TestVoteTypeEnum.TEST_GOLD

        self.getVoteService().VoteForProposal(_proposalId, _voteTypeLabel, self._backerEmail)

        self.reportResult(message='voted')

        _proposal = Proposal.get_by_id(_proposalId)

        if _proposal is not None and _proposal.votes is not None:
            self.reportResult(message='proposal has votes')

            for v in _proposal.votes:
                if v.voteType.label == TestVoteTypeEnum.TEST_GOLD:
                    self.reportResult(message='vote saved successfully')