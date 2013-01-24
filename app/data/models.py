from google.appengine.ext import db
from app.data.model.VoteType import VoteType

class Proposal(db.Model):
    name             = db.StringProperty()
    description      = db.StringProperty()
    technologiesUsed = db.StringProperty()
    status           = db.StringProperty()

class Vote(db.Model):
    userId      = db.StringProperty()
    proposal    = db.ReferenceProperty(Proposal, required=True, collection_name='votes')
    voteType    = db.ReferenceProperty(VoteType, required=True)

class Backer(db.Model):
    userId           = db.StringProperty()

class BackerVote(db.Model):
    backer          = db.ReferenceProperty(Backer, required=True, collection_name='remainingVotes')
    voteType        = db.ReferenceProperty(VoteType, required=True)
    quantity        = db.IntegerProperty()


