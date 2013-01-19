from google.appengine.ext import db

class Proposal(db.Model):
    name             = db.StringProperty()
    description      = db.StringProperty()
    technologiesUsed = db.StringProperty()
    rating           = db.IntegerProperty()

class Vote(db.Model):
    userId     = db.StringProperty()
    proposalId = db.IntegerProperty()

class Backer(db.Model):
    userId = db.StringProperty()
    gold   = db.IntegerProperty()
    silver = db.IntegerProperty()
    bronze = db.IntegerProperty()
