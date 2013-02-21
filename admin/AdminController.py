from google.appengine.ext import webapp
from google.appengine.ext.deferred import deferred
from admin.datastore_updates import initAuditing, delete_kinds
from app.decorator.ProduceJson import ProduceJson
from app.resources.RestApiResponse import RestApiResponse
from app.services.AuditService import AuditService

from app.services.VoteService import *

class AdminController(webapp.RequestHandler):

    _voteService   = VoteService()
    _backerService = BackerService()
    _auditService = AuditService()

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
            performed = False

            action = self.request.get('action')

            if action == 'clear' or action == 'resetToStable':
                self.clearDatabase()
                performed = True

            if action == 'addVoteTypes' or action == 'resetToStable':
                self._voteService.PopulateVoteTypes()
                performed = True

            if action == 'addPermissions' or action == 'resetToStable':
                self.createRolesAndPermissions()
                self.associatePermissionsWithRoles()
                performed = True

            if action == 'resetToStable':
                self.addBasicUsers()
                performed = True

            if action == 'viewPermissions':
                self.viewPermissions()
                performed = True

            if action == 'initAuditing':
                deferred.defer(delete_kinds.deleteAllForKind, kind='Audit', chained_func=initAuditing.start)
                self.response.out.write('<div>InitAuditing successfully initiated.</div>')

                return

            if performed:
                self.response.out.write('Done!')
            else:
                self.response.out.write('No Action Given!')

        except BaseException as e:
            self.response.write(str(e))

    def clearDatabase(self):
        '''
        Note: This doesn't seem a great way to do this, however this is apparently one of the recommended ways.
        See:
        https://groups.google.com/forum/?fromgroups=#!topic/google-appengine/7AgAo8qS_mk
        http://stackoverflow.com/questions/108822/delete-all-data-for-a-kind-in-google-app-engine
        '''
        kinds = ['Permission', 'Role', 'Domain', 'Proposal', 'Vote', 'VoteType', 'Backer', 'BackerVote', 'Audit']

        for kind in kinds:
            while True:
                q = db.GqlQuery("SELECT __key__ FROM " + kind)

                if q.count() <= 0:
                    break

                db.delete(q.fetch(200))

    @ProduceJson
    def viewPermissions(self):
        roles = db.GqlQuery('SELECT * FROM Role')

        return RestApiResponse.init('200', roles)

    def createRolesAndPermissions(self):
        ## Create Roles
        Role (name = 'BACKER').put()
        Role (name = 'ADMIN').put()

        ## Create Permissions
        Permission (name = 'CAN_VIEW_DOMAIN').put()
        Permission (name = 'CAN_CREATE_DOMAIN').put()
        Permission (name = 'CAN_VIEW_PROPOSAL').put()
        Permission (name = 'CAN_CREATE_PROPOSAL').put()
        Permission (name = 'CAN_VOTE').put()
        Permission (name = 'CAN_WITHDRAW').put()
        Permission (name = 'CAN_LOCK_PROPOSAL').put()
        Permission (name = 'CAN_UNLOCK_PROPOSAL').put()
        Permission (name = 'CAN_CLOSE_PROPOSAL').put()
        Permission (name = 'CAN_REOPEN_PROPOSAL').put()
        Permission (name = 'CAN_DELETE_PROPOSAL').put()
        Permission (name = 'CAN_CHANGE_OWNER').put()

    def associatePermissionsWithRoles(self):
        backerRole = Role.gql("WHERE name = 'BACKER'").get()
        adminRole  = Role.gql("WHERE name = 'ADMIN'").get()

        ## Assign Roles with Permissions
        permission = Permission.gql("WHERE name = 'CAN_VIEW_DOMAIN'").get()
        permission._roles.append(backerRole.key())
        permission._roles.append(adminRole.key())
        permission.put()

        permission = Permission.gql("WHERE name = 'CAN_CREATE_DOMAIN'").get()
        permission._roles.append(backerRole.key())
        permission._roles.append(adminRole.key())
        permission.put()

        permission = Permission.gql("WHERE name = 'CAN_VIEW_PROPOSAL'").get()
        permission._roles.append(backerRole.key())
        permission._roles.append(adminRole.key())
        permission.put()

        permission = Permission.gql("WHERE name = 'CAN_CREATE_PROPOSAL'").get()
        permission._roles.append(backerRole.key())
        #permission._roles.append(adminRole.key())
        permission.put()

        permission = Permission.gql("WHERE name = 'CAN_VOTE'").get()
        permission._roles.append(backerRole.key())
        #permission._roles.append(adminRole.key())
        permission.put()

        permission = Permission.gql("WHERE name = 'CAN_WITHDRAW'").get()
        permission._roles.append(backerRole.key())
        #permission._roles.append(adminRole.key())
        permission.put()

        permission = Permission.gql("WHERE name = 'CAN_LOCK_PROPOSAL'").get()
        permission._roles.append(backerRole.key())
        permission._roles.append(adminRole.key())
        permission.put()

        permission = Permission.gql("WHERE name = 'CAN_UNLOCK_PROPOSAL'").get()
        permission._roles.append(backerRole.key())
        permission._roles.append(adminRole.key())
        permission.put()

        permission = Permission.gql("WHERE name = 'CAN_CLOSE_PROPOSAL'").get()
        permission._roles.append(backerRole.key())
        permission._roles.append(adminRole.key())
        permission.put()

        permission = Permission.gql("WHERE name = 'CAN_REOPEN_PROPOSAL'").get()
        #permission._roles.append(backerRole.key())
        permission._roles.append(adminRole.key())
        permission.put()

        permission = Permission.gql("WHERE name = 'CAN_DELETE_PROPOSAL'").get()
        #permission._roles.append(backerRole.key())
        permission._roles.append(adminRole.key())
        permission.put()

        permission = Permission.gql("WHERE name = 'CAN_CHANGE_OWNER'").get()
        #permission._roles.append(backerRole.key())
        permission._roles.append(adminRole.key())
        permission.put()

    def addBasicUsers(self):
        try:
            # Create ADMIN account
            role = Role.gql("WHERE name = 'ADMIN'").get()
            self._backerService.CreateBacker('admin', 'Admin', 'password', role)
        except ValueError:
            pass

        try:
            # Create BACKER account
            role = Role.gql("WHERE name = 'BACKER'").get()
            self._backerService.CreateBacker('backer', 'Backer', 'password', role)
        except ValueError:
            pass