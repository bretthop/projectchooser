from google.appengine.ext import db

class Proposal(db.Model):
    name             = db.StringProperty()
    description      = db.StringProperty()
    technologiesUsed = db.StringProperty()
    status           = db.StringProperty()

class Vote(db.Model):
    userId      = db.StringProperty()
    weight      = db.IntegerProperty()
    proposal    = db.ReferenceProperty(Proposal, collection_name='votes')
    #voteType    = db.ReferenceProperty(VoteType, )


class Backer(db.Model):
    userId           = db.StringProperty()
    remaining_gold   = db.IntegerProperty()
    remaining_silver = db.IntegerProperty()
    remaining_bronze = db.IntegerProperty()

class BackerVote(db.Model):
    #backers         = db.ReferenceProperty(Backer, required=True, collection_name='remainingVotes')
    #voteType        = db.ReferenceProperty(VoteType, required=True)
    quantity        = db.IntegerProperty()

class VoteType(db.Model):
    weight          = db.IntegerProperty()
    label           = db.StringProperty()
