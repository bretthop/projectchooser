from app.test.cases.BaseUnitTest import BaseUnitTest

from app.data.models import VoteType
from app.data.enums.VoteTypeEnum import VoteTypeEnum

class DBFixtures(BaseUnitTest):

    def test_populateAllVoteTypes(self):
        vt = VoteType()
        vt.label = VoteTypeEnum.GOLD
        vt.weight = 8
        vt.put()

        vt = VoteType()
        vt.label = VoteTypeEnum.SILVER
        vt.weight = 5
        vt.put()

        vt = VoteType()
        vt.label = VoteTypeEnum.BRONZE
        vt.weight = 3
        vt.put()

        self.reportResult(message='PASS')