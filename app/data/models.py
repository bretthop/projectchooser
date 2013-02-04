from google.appengine.ext import db
from app.data.model.VoteType import VoteType
from app.data.model.Domain import Domain

class Permission(db.Model):
    name = db.StringProperty()

#    TODO: Adding this property causes an infinite recursion when trying to serialise a role object (FIX!)
#    @property
#    def roles(self):
#        return Role.gql("WHERE _permissionKeys = :1", self.key())

class Role(db.Model):
    name            = db.StringProperty()
    _permissionKeys = db.ListProperty(db.Key)

    @property
    def permissions(self):
        permissions = []

        for key in self._permissionKeys:
            permission = Permission.get(key)
            permissions.append(permission)

        return permissions

class Backer(db.Model):
    email            = db.StringProperty()
    username         = db.StringProperty()
    password         = db.StringProperty()
    role             = db.ReferenceProperty(Role, required = True)

class Proposal(db.Model):
    name             = db.StringProperty()
    description      = db.StringProperty()
    technologiesUsed = db.StringProperty()
    status           = db.StringProperty(default = 'OPEN')
    owner            = db.ReferenceProperty(Backer)
    domain           = db.ReferenceProperty(Domain, required=False)
    created          = db.DateTimeProperty(auto_now_add=True)
    updated          = db.DateTimeProperty(auto_now_add=True, auto_now=True)

class Vote(db.Model):
    userId      = db.StringProperty()
    proposal    = db.ReferenceProperty(Proposal, required=True, collection_name='votes')
    voteType    = db.ReferenceProperty(VoteType, required=True)
    created     = db.DateTimeProperty(auto_now_add=True)

class BackerVote(db.Model):
    backer          = db.ReferenceProperty(Backer, required=True, collection_name='remainingVotes')
    voteType        = db.ReferenceProperty(VoteType, required=True)
    quantity        = db.IntegerProperty()