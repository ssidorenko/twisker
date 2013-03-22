import datetime
import random

from google.appengine.ext import ndb, deferred
from google.appengine.api import memcache, taskqueue

from flask_login import UserMixin

from twisker.task_utils import get_interval_number

from twisker.models import Twisk

# Max interval at which feeds can be updated
UPDATE_INTERVAL = 10

# Memcache and taskqueue namespace to store the user feeds in
USER_FEED_NAMESPACE = "userfeed"


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
        """Returns and cache the users feed (last twisks from the users they follow)"""
        # First try to return the cached one
        feed = memcache.get(self.key.id(), namespace=USER_FEED_NAMESPACE)

        if feed is not None:
            return feed

        return self.update_feed()

    def update_feed(self):
        """Update the memcache for this user feed"""
        if self.following:
            feed = Twisk.gql("WHERE author in :1 ORDER BY when DESC LIMIT 50",
                             self.following + [self.key, ])
        else:
            feed = []

        memcache.set(self.key.id(), list(feed), namespace=USER_FEED_NAMESPACE)

        return feed

    def update_feeds(self):
        """Update the feeds for all of the user's followers (should be called
            in a background task)"""

        for k in self.followers + [self.key, ]:
            # For each follower, schedule a task with a name unique for this
            # user for UPDATE_INTERVAL seconds

            # interval_num is going to change every UPDATE_INTERVAL seconds
            interval_num = get_interval_number(datetime.datetime.now(), UPDATE_INTERVAL)

            # Generate task name for this user and this interval
            task_name = '-'.join([str(el) for el in [USER_FEED_NAMESPACE,
                                                     k.id(), interval_num]])
            try:
                deferred.defer(TwiskUser.deferred_update_feed, k,
                               _name=task_name,
                               _countdown=5 + random.randint(0, 5))

            # If this tasks already exists it means that this method has already
            # been scheduled less than UPDATE_INTERVAL seconds ago
            except (taskqueue.TaskAlreadyExistsError, taskqueue.TombstonedTaskError):
                pass

    @classmethod
    def deferred_update_feed(cls, user_key):
        user_key.get().update_feed()
