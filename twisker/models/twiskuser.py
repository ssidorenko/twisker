from google.appengine.ext import ndb


class TwiskUser(ndb.Model):
    """Represents an user. Their username is the key"""

    followers = ndb.KeyProperty(kind='TwiskUser', repeated=True)
    following = ndb.KeyProperty(kind='TwiskUser', repeated=True)

    # TODO find another way to realise this without hitting the 5 write/s limit
    @ndb.transactional(xg=True)
    def follow(self, other_username):
        other_user = TwiskUser.get_by_id(other_username)

        if other_user.key != self.key and other_user.key not in self.following:
            other_user.followers.append(self.key)
            self.following.append(other_user.key)
            other_user.put()
            self.put()
