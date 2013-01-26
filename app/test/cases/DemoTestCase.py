import unittest

from google.appengine.ext import testbed
#from app.test.testModels import MyTestModel

class DemoTestCase(unittest.TestCase):

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def testInsertEntity(self):
        MyTestModel().put()
        #self.assertEqual(1, len(MyTestModel.all().fetch(2)))

if __name__ == '__main__':
    unittest.main()
