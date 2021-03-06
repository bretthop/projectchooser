from google.appengine.ext import db
from app.data.model.VoteType import VoteType
from app.data.model.Domain import Domain

class Permission(db.Model):
    name = db.StringProperty()
    _roles = db.ListProperty(db.Key)

#    TODO: Adding this property causes an infinite recursion when trying to serialise a role object (FIX!)
#    @property
#    def roles(self):
#        return Role.gql("WHERE _permissionKeys = :1", self.key())

class Role(db.Model):
    name            = db.StringProperty()

    @property
    def permissions(self):
        permissions = Permission.gql('WHERE _roles = :1', self.key())
        return permissions

class Backer(db.Expando):
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
    domain           = db.ReferenceProperty(Domain, required=True, collection_name='proposals')
    created          = db.DateTimeProperty(auto_now_add=True)
    updated          = db.DateTimeProperty(auto_now_add=True, auto_now=True)

    @property
    def totalRating(self):
        """
        Return proposal's total weight (sum of all weights of all votes)
        """
        result = 0
        for v in self.votes:
            result += v.voteType.weight

        return result


class Vote(db.Expando):
    backer      = db.ReferenceProperty(Backer, required=False)
    proposal    = db.ReferenceProperty(Proposal, required=True, collection_name='votes')
    voteType    = db.ReferenceProperty(VoteType, required=True)
    created     = db.DateTimeProperty(auto_now_add=True)

class BackerVote(db.Model):
    backer          = db.ReferenceProperty(Backer, required=True, collection_name='remainingVotes')
    voteType        = db.ReferenceProperty(VoteType, required=True)
    quantity        = db.IntegerProperty()

class Audit(db.Model):
    domain = db.ReferenceProperty(Domain, required=False)
    proposal = db.ReferenceProperty(Proposal, required=False)
    backer = db.ReferenceProperty(Backer, required=False)
    message = db.StringProperty()
    dateCreated = db.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def dateDesc(a, b):
        return cmp(b.dateCreated, a.dateCreated)