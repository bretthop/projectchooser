from google.appengine.ext import db
from app.data.model.VoteType import VoteType
from app.data.model.Domain import Domain

class Backer(db.Model):
    userId           = db.StringProperty()

class Proposal(db.Model):
    name             = db.StringProperty()
    description      = db.StringProperty()
    technologiesUsed = db.StringProperty()
    status           = db.StringProperty(default = 'OPEN')
    owner            = db.ReferenceProperty(Backer)
    domain           = db.ReferenceProperty(Domain, required=False)

class Vote(db.Model):
    userId      = db.StringProperty()
    proposal    = db.ReferenceProperty(Proposal, required=True, collection_name='votes')
    voteType    = db.ReferenceProperty(VoteType, required=True)

class BackerVote(db.Model):
    backer          = db.ReferenceProperty(Backer, required=True, collection_name='remainingVotes')
    voteType        = db.ReferenceProperty(VoteType, required=True)
    quantity        = db.IntegerProperty()