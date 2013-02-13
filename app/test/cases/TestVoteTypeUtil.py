from app.test.cases.BaseUnitTest import BaseUnitTest

from app.data.enums.VoteTypeEnum import VoteTypeEnum
from app.util.VoteTypeUtil import VoteTypeUtil

class TestVoteTypeUtil(BaseUnitTest):

    def test_getVoteTypeByLabel(self):
        testVoteTypeLabel = VoteTypeEnum.GOLD

        _readVoteType = VoteTypeUtil.GetVoteTypeByLabel(testVoteTypeLabel)

        self.assertIsNotNone(_readVoteType, 'VoteType is None')

        self.assertTrue(_readVoteType.label == testVoteTypeLabel, 'Fetched Vote type not matching the expected value')

        self.reportResult(message='PASS')