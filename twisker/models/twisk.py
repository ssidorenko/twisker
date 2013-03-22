import datetime
import random
import logging

from google.appengine.ext import ndb, deferred
from google.appengine.api import memcache, taskqueue

from twisker.task_utils import get_interval_number
from tag import Tag

# Max interval at which tag feeds can be updated
UPDATE_INTERVAL = 10

# Memcache and taskqueu namespace to store the tag feeds in
TAG_FEED_NAMESPACE = "tagfeed"


class Twisk(ndb.Model):
    content = ndb.StringProperty(required=True)
    when = ndb.DateTimeProperty(auto_now_add=True)
    author = ndb.KeyProperty(kind='TwiskUser')
    tags = ndb.StringProperty(repeated=True)

    def _pre_put_hook(self):
        self.parse_tags()

    def _post_put_hook(self, future):
        """Updates the feeds of the followers once a twisk has been posted"""
        self.author.get().update_feeds()
        self.update_tag_feeds()

    def parse_tags(self):
        """Reads self.content and each found hashtag"""
        for word in self.content.split(" "):
            if word.startswith('#'):
                self.add_tag(word[1:])

    def add_tag(self, tag):
        """Add a tag to self.tags and increment the corresponding tag counter"""
        logging.debug("adding tag {}".format(tag))
        if tag.isalnum() and tag not in self.tags:
            # Keep track of how many times tag has been referenced
            Tag.incr(tag)
            self.tags.append(tag)

    def _pre_delete_hook(self):
        """Decrement the tag counter before deleting the twisk"""
        for tag in self.tags:
            Tag.decr(tag)

    def update_tag_feeds(self):
        """Update the tag feed for each tags in this Twisk"""
        # FIXME should be factored with TwiskUser.update_feeds and Tag.sched_flush
        for tag in self.tags:
            interval_num = get_interval_number(datetime.datetime.now(), UPDATE_INTERVAL)

            # Generate task name for this tag and this interval
            task_name = '-'.join([str(el) for el in [TAG_FEED_NAMESPACE,
                                  tag, interval_num]])
            try:
                deferred.defer(Twisk.update_tag_feed, tag, _name=task_name,
                               _countdown=5 + random.randint(0, 5))

            # If this tasks already exists it means that this method has already
            # been scheduled less than UPDATE_INTERVAL seconds ago
            except (taskqueue.TaskAlreadyExistsError, taskqueue.TombstonedTaskError):
                pass

    @classmethod
    def get_tag_feed(cls, tag):
        """Returns a list of twisks tagged with the given tag"""
        feed = memcache.get("tag", namespace=TAG_FEED_NAMESPACE)

        if feed is not None:
            return feed

        return cls.update_tag_feed(tag)

    @classmethod
    def update_tag_feed(cls, tag):
        """Updates the cached feed for a given tag"""
        feed = Twisk.gql("WHERE tags = :1 ORDER BY when DESC LIMIT 50", tag)

        memcache.set(tag, list(feed), namespace=TAG_FEED_NAMESPACE)

        return feed
