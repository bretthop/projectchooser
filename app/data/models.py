from google.appengine.ext import db

class Proposal(db.Model):
    name             = db.StringProperty()
    description      = db.StringProperty()
    technologiesUsed = db.StringProperty()

class Vote(db.Model):
    userId     = db.StringProperty()
    proposalId = db.IntegerProperty()
    weight     = db.IntegerProperty()

class Backer(db.Model):
    userId           = db.StringProperty()
    remaining_gold   = db.IntegerProperty()
    remaining_silver = db.IntegerProperty()
    remaining_bronze = db.IntegerProperty()
