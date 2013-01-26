import unittest2
from app.test.cases.TestVoteService import TestVoteService

class TestSuite(unittest2.TestSuite):

    def load_tests(self, tests, pattern):
        suite = unittest2.TestSuite()
        case1 = self.loadTestsFromTestCase(TestVoteService)
        suite.addTests(case1)

        return suite