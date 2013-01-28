import os
import unittest2

class BaseUnitTest(unittest2.TestCase):
    def setUp(self):
        app_id = 'projectchooser'
        os.environ['APPLICATION_ID'] = app_id
        datastore_file = 'C:\Users\Sini\AppData\Local\Temp\dev_appserver.datastore'
        from google.appengine.api import apiproxy_stub_map,datastore_file_stub
        apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
        stub = datastore_file_stub.DatastoreFileStub(app_id, datastore_file, '/')
        apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)

    def tearDown(self):
        pass

    def reportResult(self, message = ''):
        print '[PASS] ' + self._testMethodName + (message if message != '' else '')

#    if __name__ == '__main__':
#        unittest2.main()
