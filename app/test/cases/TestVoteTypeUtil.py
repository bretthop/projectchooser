from app.test.cases.BaseUnitTest import BaseUnitTest

from app.test.fixtures.TestVoteTypeEnum import TestVoteTypeEnum
from app.util.VoteTypeUtil import VoteTypeUtil

class TestVoteTypeUtil(BaseUnitTest):

    def test_getVoteTypeByLabel(self):
        testVoteTypeLabel = TestVoteTypeEnum.TEST_GOLD

        _readVoteType = VoteTypeUtil.GetVoteTypeByLabel(testVoteTypeLabel)

        if _readVoteType.label == testVoteTypeLabel:
            self.reportResult()