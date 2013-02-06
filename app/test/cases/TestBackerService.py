from app.test.cases.BaseUnitTest import BaseUnitTest

from app.services.BackerService import BackerService
from app.data.models import Role

class TestBackerService(BaseUnitTest):

    _backerService = None

    #singleton pattern
    def getBackerService(self):
        if self._backerService is None:
            self._backerService = BackerService()

        return self._backerService

    def test_getBackerByEmail(self):
        _backerEmail = 'test_backer_2013-01-29@project.chooser.com.au'
        _backerUsername = 'test_backer_2013-01-29'
        _backerPassword = 'password'
        _backerRole = Role(name='BACKER').put()

        _backer = self.getBackerService().CreateBacker(_backerEmail, _backerUsername, _backerPassword, _backerRole)

        #_backer = self.getBackerService().GetBackerByEmail(_backerEmail)

        if _backer is not None:
            self.reportResult()