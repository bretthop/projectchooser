from google.appengine.ext import webapp
from app.decorator.ProduceJson import JsonListResult

from app.services.VoteService import *

class AdminController(webapp.RequestHandler):

    _voteService   = VoteService()
    _backerService = BackerService()

    def post(self):
        try :
            action = self.request.get('action')

            if action == 'ADD_USER':
                email       = self.request.get('email')
                username    = self.request.get('username')
                password    = self.request.get('password')
                roleName    = self.request.get('role')

                role = Role.gql("WHERE name = '%s'" % roleName).get()

                self._backerService.CreateBacker(email, username, password, role)

                self.response.out.write('Done!')
            else:
                self.response.out.write('No Action!')
        except BaseException as e:
            self.response.write(str(e))
    def get(self):
        try:
            action = self.request.get('action')

            if action == 'addVoteTypes':
                self._voteService.PopulateVoteTypes()

            elif action == 'clear':
                self.clearDatabase()

            elif action == 'resetToStable':
                self.clearDatabase()
                self._voteService.PopulateVoteTypes()
            elif action == 'addPermissions':
                self.addPermissions()
            elif action == 'viewPermissions':
                self.viewPermissions()

            self.response.out.write('Done!')
        except BaseException as e:
            self.response.write(str(e))

    def clearDatabase(self):
        '''
        Note: This doesn't seem a great way to do this, however this is apparently one of the recommended ways.
        See:
        https://groups.google.com/forum/?fromgroups=#!topic/google-appengine/7AgAo8qS_mk
        http://stackoverflow.com/questions/108822/delete-all-data-for-a-kind-in-google-app-engine
        '''
        kinds = ['Permission', 'Role', 'Domain', 'Proposal', 'Vote', 'VoteType', 'Backer', 'BackerVote']

        for kind in kinds:
            while True:
                q = db.GqlQuery("SELECT __key__ FROM " + kind)

                if q.count() <= 0:
                    break

                db.delete(q.fetch(200))

    @JsonListResult
    def viewPermissions(self):
        roles = db.GqlQuery('SELECT * FROM Role').fetch(100)

        return roles


    def addPermissions(self):
        ## Create Permissions
        canCreateProposalPermission = Permission (
            name = 'CAN_CREATE_PROPOSAL'
        )
        canCreateProposalPermission.put()

        canVotePermission = Permission (
            name = 'CAN_VOTE'
        )
        canVotePermission.put()

        canWithdrawPermission = Permission (
            name = 'CAN_WITHDRAW'
        )
        canWithdrawPermission.put()

        canLockProposalPermission = Permission (
            name = 'CAN_LOCK_PROPOSAL'
        )
        canLockProposalPermission.put()

        canUnlockProposalPermission = Permission (
            name = 'CAN_UNLOCK_PROPOSAL'
        )
        canUnlockProposalPermission.put()

        canCloseProposalPermission = Permission (
            name = 'CAN_CLOSE_PROPOSAL'
        )
        canCloseProposalPermission.put()

        canReopenProposalPermission = Permission (
            name = 'CAN_REOPEN_PROPOSAL'
        )
        canReopenProposalPermission.put()

        canDeleteProposalPermission = Permission (
            name = 'CAN_DELETE_PROPOSAL'
        )
        canDeleteProposalPermission.put()

        canChangeOwnerPermission = Permission (
            name = 'CAN_CHANGE_OWNER'
        )
        canChangeOwnerPermission.put()

        ## Create Roles (ad assign permissions to roles)
        backerRole = Role (
            name = 'BACKER',
            _permissionKeys = [
                canCreateProposalPermission.key(),
                canVotePermission.key(),
                canWithdrawPermission.key(),
                canLockProposalPermission.key(),
                canUnlockProposalPermission.key(),
                canCloseProposalPermission.key()
            ]
        )
        backerRole.put()

        adminRole = Role (
            name = 'ADMIN',
            _permissionKeys = [
                canLockProposalPermission.key(),
                canUnlockProposalPermission.key(),
                canCloseProposalPermission.key(),
                canReopenProposalPermission.key(),
                canDeleteProposalPermission.key(),
                canChangeOwnerPermission.key()
            ]
        )
        adminRole.put()