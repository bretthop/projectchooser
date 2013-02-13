from app.test.cases.BaseUnitTest import BaseUnitTest

from app.services.ProposalService import ProposalService

from app.data.models import Proposal
from app.data.model.Domain import Domain

class TestProposalService(BaseUnitTest):

    _proposalService = None
    _testDomainName = 'TEST DOMAIN #1'
    _testProposalName = 'TEST PROPOSAL #1'

    #singleton pattern
    def getProposalService(self):
        if self._proposalService is None:
            self._proposalService = ProposalService()

        return self._proposalService

    def test_createNewProposal(self):
        _domain = Domain(
            title = self._testDomainName,
            description = self._testDomainName,
        ).put()

        domain = Domain.get_by_id(_domain.id())

        self.assertIsNotNone(domain.key().id(), 'Domain ID is None')

        _proposal = Proposal(
            name = self._testProposalName,
            description = 'DESCRIPTION OF ' + self._testProposalName,
            technologiesUsed = 'TECHNOLOGIES USER IN ' + self._testProposalName,
            status = 'OPEN',
            domain = _domain
        )

        self.getProposalService().saveProposal(_proposal)

        self.assertIsNotNone(_proposal.key().id(), 'Proposal ID is None')
        self.assertIsNotNone(_proposal.domain, 'Proposal\'s Domain is None')

        self.assertTrue(_proposal.name == self._testProposalName, 'Fetched Proposal not matching the expected value')

        self.reportResult(message='PASS')

    def test_getProposalsByStatusOpen(self):
        _domain = Domain(
            title = self._testDomainName,
            description = self._testDomainName,
        ).put()

        domain = Domain.get_by_id(_domain.id())

        Proposal(
            name = self._testProposalName,
            description = 'DESCRIPTION OF ' + self._testProposalName,
            technologiesUsed = 'TECHNOLOGIES USER IN ' + self._testProposalName,
            status = 'OPEN',
            domain = domain
        ).put()

        _proposals = self.getProposalService().GetProposalsByDomainAndStatus(domain.key().id(), 'OPEN')

        self.assertIsNotNone(_proposals, 'No Proposals found')

        self.assertTrue(_proposals.count() == 1, 'Found 0 proposals (expected 1)')

        self.reportResult(message='PASS')

    def test_getProposalsByStatusClosed(self):
        _domain = Domain(
            title = self._testDomainName,
            description = self._testDomainName,
        ).put()

        domain = Domain.get_by_id(_domain.id())

        Proposal(
            name = self._testProposalName,
            description = 'DESCRIPTION OF ' + self._testProposalName,
            technologiesUsed = 'TECHNOLOGIES USER IN ' + self._testProposalName,
            status = 'OPEN',
            domain = domain
        ).put()

        _proposals = self.getProposalService().GetProposalsByDomainAndStatus(domain.key().id(), 'CLOSED')

        self.assertIsNotNone(_proposals, 'No Proposals found')

        self.assertTrue(_proposals.count() == 0, 'Found 1 or more proposals (expected 0)')

        self.reportResult(message='PASS')
