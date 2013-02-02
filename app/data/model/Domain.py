from google.appengine.ext import db

class Domain(db.Model):
  title       = db.StringProperty(required=False)
  description = db.StringProperty(required=False)
  status      = db.StringProperty(required=True, default = 'OPEN')