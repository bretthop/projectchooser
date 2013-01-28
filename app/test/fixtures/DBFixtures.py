from app.test.cases.BaseUnitTest import BaseUnitTest

from app.data.models import VoteType
from app.test.fixtures.TestVoteTypeEnum import TestVoteTypeEnum

class DBFixtures(BaseUnitTest):

    def test_populateAllVoteTypes(self):
        vt = VoteType()
        vt.label = TestVoteTypeEnum.TEST_GOLD
        vt.weight = 8
        vt.put()

        vt = VoteType()
        vt.label = TestVoteTypeEnum.TEST_SILVER
        vt.weight = 5
        vt.put()

        vt = VoteType()
        vt.label = TestVoteTypeEnum.TEST_BRONZE
        vt.weight = 3
        vt.put()

        self.reportResult()