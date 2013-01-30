from app.test.cases.BaseUnitTest import BaseUnitTest

from app.data.enums.VoteTypeEnum import VoteTypeEnum
from app.util.VoteTypeUtil import VoteTypeUtil

class TestVoteTypeUtil(BaseUnitTest):

    def test_getVoteTypeByLabel(self):
        testVoteTypeLabel = VoteTypeEnum.GOLD

        _readVoteType = VoteTypeUtil.GetVoteTypeByLabel(testVoteTypeLabel)

        if _readVoteType.label == testVoteTypeLabel:
            self.reportResult()