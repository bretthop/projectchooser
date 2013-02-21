from app.test.cases.BaseUnitTest import BaseUnitTest

from google.appengine.ext import db

from app.data.models import Proposal
from app.data.model.Domain import Domain
from app.data.enums.VoteTypeEnum import VoteTypeEnum
from app.util.VoteTypeUtil import VoteTypeUtil

from app.services.BackerService import BackerService
from app.services.ProposalService import ProposalService
from app.services.VoteService import VoteService

class TestVoteService(BaseUnitTest):

    _backerService   = None
    _proposalService = None
    _voteService     = None
    _testDomainName = 'TEST DOMAIN #1'
    _testProposalName = 'TEST PROPOSAL #1'
    _backerEmail = 'test_backer_2013-01-29@project.chooser.com.au'
    _voteTypeLabelG = VoteTypeEnum.GOLD
    _voteTypeLabelS = VoteTypeEnum.SILVER

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

    #singleton pattern
    def getVoteService(self):
        if self._backerService is None:
            self._backerService = BackerService()

        return self._backerService

    def test_voteForProposal(self):
        _domain = Domain(
            title = self._testDomainName,
            description = self._testDomainName,
        ).put()

        domain = Domain.get_by_id(_domain.id())

        self.assertTrue(domain.key().id() is not None, 'Domain ID is None')

        _proposal = Proposal(
            name = self._testProposalName,
            description = 'DESCRIPTION OF ' + self._testProposalName,
            technologiesUsed = 'TECHNOLOGIES USER IN ' + self._testProposalName,
            status = 'OPEN',
            domain = _domain
        )

        self.getProposalService().saveProposal(_proposal)

        self.assertIsNotNone(_proposal, 'Proposal is None')

        self.getVoteService().VoteForProposal(_proposal.key().id(), self._voteTypeLabelG, self._backerEmail)

        self.assertTrue(_proposal.votes.count() > 0, 'Proposal has no votes')

        _voteFound = False
        for v in _proposal.votes:
            if v.voteType.label == VoteTypeEnum.GOLD:
                _voteFound = True

        self.assertTrue(_voteFound, 'Failed to vote for proposal')

        self.reportResult(message='PASS')

    def test_withdrawVote(self):
        self.reportResult(message='Starting test_withdrawVote')

        _domain = Domain(
            title = self._testDomainName,
            description = self._testDomainName,
        ).put()

        domain = Domain.get_by_id(_domain.id())

        self.assertTrue(domain.key().id() is not None, 'Domain ID is None')

        _proposal = Proposal(
            name = self._testProposalName,
            description = 'DESCRIPTION OF ' + self._testProposalName,
            technologiesUsed = 'TECHNOLOGIES USER IN ' + self._testProposalName,
            status = 'OPEN',
            domain = _domain
        )

        _backer = self._backerService.GetBackerByEmail(self._backerEmail)

        self.getProposalService().saveProposal(_proposal)

        self.assertIsNotNone(_proposal, 'Proposal is None')

        self.getVoteService().VoteForProposal(_proposal.key().id(), self._voteTypeLabelS, self._backerEmail)

        self.assertTrue(_proposal.votes.count() > 0, 'Proposal has no votes')

        _voteId = db.GqlQuery("SELECT __key__ FROM Vote WHERE proposal = :pProposal AND backer = :pBacker AND voteType = :pVoteType",
            pProposal = _proposal,
            pBacker   = _backer,
            pVoteType = VoteTypeUtil.GetVoteTypeByLabel(self._voteTypeLabelS)
        ).get().id()

        self.assertIsNotNone(_voteId, 'Vote is None')

        self.getVoteService().WithdrawVote(_voteId, self._backerEmail)

        self.assertTrue(_proposal.votes.count() == 0, 'Failed to withdraw vote')

        self.reportResult(message='PASS')