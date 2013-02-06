from app.test.cases.BaseUnitTest import BaseUnitTest

from app.services.ProposalService import ProposalService

from app.data.models import Proposal
from app.data.model.Domain import Domain

class TestProposalService(BaseUnitTest):

    _proposalService = None
    _testDomainName = 'TEST DOMAIN TITLE #1'

    #singleton pattern
    def getProposalService(self):
        if self._proposalService is None:
            self._proposalService = ProposalService()

        return self._proposalService

    def test_createNewProposal(self):
        _domain = Domain(
            title = self._testDomainName,
            description = 'TEST DOMAIN DESCRIPTION #1',
        ).put()

        _testProposalName = 'TEST PROPOSAL #1'

        _proposal = Proposal(
            name = _testProposalName,
            description = 'DESCRIPTION OF ' + _testProposalName,
            technologiesUsed = 'TECHNOLOGIES USER IN ' + _testProposalName,
            status = 'OPEN',
            domain = _domain
        )

        result = self.getProposalService().saveProposal(_proposal)

        if result.name == _testProposalName:
            self.reportResult()

    def test_getProposalsByStatusOpen(self):
        domainId = Domain.gql("WHERE title = :pTitle", pTitle=self._testDomainName).get().key().id()
        _proposals = self.getProposalService().GetProposalsByDomainAndStatus(domainId, 'OPEN')

        if _proposals is not None:
            self.reportResult(message=' count='+str(_proposals.count()))
            if _proposals.count() > 0:
                self.reportResult()

    def test_getProposalsByStatusClosed(self):
        domainId = Domain.gql("WHERE title = :pTitle", pTitle=self._testDomainName).get().key().id()
        _proposals = self.getProposalService().GetProposalsByDomainAndStatus(domainId, 'CLOSED')

        if _proposals is not None:
            self.reportResult(message=' count='+str(_proposals.count()))
            if _proposals.count() == 0:
                self.reportResult()
