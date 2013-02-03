from google.appengine.ext import db

class Domain(db.Model):
  title       = db.StringProperty(required=False)
  description = db.StringProperty(required=False)
  status      = db.StringProperty(required=True, default = 'OPEN')
  created     = db.DateTimeProperty(auto_now_add=True)
  updated     = db.DateTimeProperty(auto_now_add=True, auto_now=True)