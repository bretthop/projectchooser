import unittest2
from app.test.cases.TestVoteTypeUtil import TestVoteTypeUtil

from app.test.cases.TestProposalService import TestProposalService
from app.test.cases.TestBackerService import TestBackerService
from app.test.cases.TestVoteService import TestVoteService

from app.test.fixtures.DBFixtures import DBFixtures

class TestSuite(unittest2.TestSuite):

    def load_tests(self, tests, pattern):
        suite = unittest2.TestSuite()
        case001 = self.loadTestsFromTestCase(DBFixtures)
        suite.addTests(case001)

        case101 = self.loadTestsFromTestCase(TestVoteTypeUtil)
        suite.addTests(case101)

        case110 = self.loadTestsFromTestCase(TestBackerService)
        suite.addTests(case110)

        case120 = self.loadTestsFromTestCase(TestProposalService)
        suite.addTests(case120)

#TODO: check why proposal.votes collection is empty after voting
#        case130 = self.loadTestsFromTestCase(TestVoteService)
#        suite.addTests(case130)


        return suite