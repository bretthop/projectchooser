from google.appengine.ext import db

class VoteType(db.Model):
    weight          = db.IntegerProperty()
    label           = db.StringProperty()