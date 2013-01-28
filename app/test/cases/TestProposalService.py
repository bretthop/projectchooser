from app.test.cases.BaseUnitTest import BaseUnitTest

from app.services.ProposalService import ProposalService

from app.data.models import Proposal

class TestProposalService(BaseUnitTest):

    _proposalService = None

    #singleton pattern
    def getProposalService(self):
        if self._proposalService is None:
            self._proposalService = ProposalService()

        return self._proposalService

    def test_createNewProposal(self):
        _testProposalName = 'TEST PROPOSAL #1'

        _proposal = Proposal(
            name = _testProposalName,
            description = 'DESCRIPTION OF ' + _testProposalName,
            technologiesUsed = 'TECHNOLOGIES USER IN ' + _testProposalName,
            status = 'OPEN'
        )

        result = self.getProposalService().saveProposal(_proposal)

        if result.name == _testProposalName:
            self.reportResult()

    def test_getProposalsByStatusOpen(self):
        _proposals = self.getProposalService().GetProposalsByStatus('OPEN')

        if _proposals is not None:
            self.reportResult(message=' count='+str(_proposals.count()))
            if _proposals.count() > 0:
                self.reportResult()

    def test_getProposalsByStatusClosed(self):
        _proposals = self.getProposalService().GetProposalsByStatus('CLOSED')

        if _proposals is not None:
            self.reportResult(message=' count='+str(_proposals.count()))
            if _proposals.count() == 0:
                self.reportResult()
