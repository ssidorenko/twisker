from google.appengine.ext import db

class Twisk(db.Model):
    content = db.StringProperty(required = True)
    when = db.DateTimeProperty(auto_now_add = True)
    author = db.UserProperty(required = True)
