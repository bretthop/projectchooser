import os
import unittest2

from google.appengine.api import datastore
from app.data.models import Proposal

class BaseUnitTest(unittest2.TestCase):
    def setUp(self):
        self.reportResult(message=' >>> set up')
        app_id = 'projectchooser'
        os.environ['APPLICATION_ID'] = app_id
        datastore_file = 'C:\Users\Sini\AppData\Local\Temp\dev_appserver.datastore'
        from google.appengine.api import apiproxy_stub_map,datastore_file_stub
        apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
        stub = datastore_file_stub.DatastoreFileStub(app_id, datastore_file, '/')
        apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)

    def tearDown(self):
        self.reportResult(message=' >>> tear down')
        # Delete all Vote entities
        query = datastore.Query(kind='Vote', keys_only=True)
        results = query.Get(100)
        while results:
            print "Deleting %d %s entities" % (len(results), 'Vote')
            datastore.Delete(results)
            results = query.Get(100)

        # Delete all Proposal entities
        query = datastore.Query(kind='Proposal', keys_only=True)
        results = query.Get(100)
        while results:
            print "Deleting %d %s entities" % (len(results), 'Proposal')
            datastore.Delete(results)
            results = query.Get(100)

        # Delete all Domain entities
        query = datastore.Query(kind='Domain', keys_only=True)
        while results:
            print "Deleting %d %s entities" % (len(results), 'Domain')
            datastore.Delete(results)
            results = query.Get(100)

    def reportResult(self, message = ''):
        print '[ECHO] ' + self._testMethodName + (' ' + message if message != '' else '')

#    if __name__ == '__main__':
#        unittest2.main()
