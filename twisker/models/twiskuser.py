from google.appengine.ext import ndb
from google.appengine.api import memcache
from flask_login import UserMixin
from twisk import Twisk


class TwiskUser(ndb.Model, UserMixin):
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

    # Here follows flask-login required methods

    def get_id(self):
        """Simple wrapper for flask-login"""
        return self.key.id()

    def get_feed(self):
        """Returns and cache the users feed"""
        # First try to return the cached one
        feed = memcache.get(self.key.id(), namespace="feed")

        if feed:
            return feed

        return self.update_feed()

    def update_feed(self):
        if self.following:
            feed = Twisk.gql("WHERE author in :1 ORDER BY when DESC LIMIT 50", self.following)
        else:
            feed = []

        memcache.set(self.key.id(), list(feed), namespace="feed")

        return feed
