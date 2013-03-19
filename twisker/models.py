from google.appengine.ext import db

class TwiskUser(db.Model):
    followers = db.ListProperty(db.Key)
    following = db.ListProperty(db.Key)

    # TODO find another way to realise this without hitting the 5 write/s limit
    @db.transactional(xg=True)
    def follow(self, other_username):
        other_user = TwiskUser.get_by_key_name(other_username)

        if other_user.key() != self.key() and other_user.key() not in self.following:
            other_user.followers.append(self.key())
            self.following.append(other_user.key())
            other_user.put()
            self.put()

class Twisk(db.Model):
    content = db.StringProperty(required = True)
    when = db.DateTimeProperty(auto_now_add = True)
    author = db.ReferenceProperty(TwiskUser)
