from BaseUnitTest import BaseUnitTest

from app.data.model.VoteType import VoteType
from app.util.VoteTypeUtil import VoteTypeUtil

class TestVoteService(BaseUnitTest):

    def test_createVoteType(self):
        testVoteTypeLabel = 'TEST_GOLD'

        _createdVoteType = VoteType(
            label = testVoteTypeLabel,
            weight = 10
        )

        _createdVoteType.put()

        if _createdVoteType.key() is not None and _createdVoteType.key().id() is not None:
            self.reportResult()

    def test_getVoteTypeByLabel(self):
        testVoteTypeLabel = 'TEST_GOLD'

        _readVoteType = VoteTypeUtil.GetVoteTypeByLabel(testVoteTypeLabel)

        if _readVoteType.label == testVoteTypeLabel:
            self.reportResult()