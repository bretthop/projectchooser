import unittest2
from app.test.cases.TestVoteTypeUtil import TestVoteTypeUtil
from app.test.cases.TestProposalService import TestProposalService
from app.test.fixtures.DBFixtures import DBFixtures

class TestSuite(unittest2.TestSuite):

    def load_tests(self, tests, pattern):
        suite = unittest2.TestSuite()
        case001 = self.loadTestsFromTestCase(DBFixtures)
        suite.addTests(case001)

        case101 = self.loadTestsFromTestCase(TestVoteTypeUtil)
        suite.addTests(case101)

        case102 = self.loadTestsFromTestCase(TestProposalService)
        suite.addTests(case102)

        return suite