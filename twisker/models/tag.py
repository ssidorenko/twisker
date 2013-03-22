import datetime
import random

from google.appengine.api import memcache, taskqueue
from google.appengine.ext import ndb, deferred

from twisker.task_utils import get_interval_number

# At which interval should counters be flushed to datastore
INTERVAL = 10


class Tag(ndb.Model):
    """Represents an existing tag. The keyname is the tag. count is a cached counter
    which holds the amount of twisks tagged with this tag."""

    count = ndb.IntegerProperty(default=0)

    def _pre_delete_hook(self):
        memcache.delete(self.key.id(), self._get_kind())

    def hashtag(self):
        """Returns the tag prefixed with an hash"""
        return "#" + self.key.id()

    @classmethod
    def get_value(cls, name):
        """Returns the value of the counter with the specified name."""
        # First, do a cache lookup
        cached_count = memcache.get(name, cls._get_kind())

        if cached_count is not None:
            return cached_count

        # Then, do a db lookup
        counter = cls.get_by_id(name)

        if counter:
            count = counter.count

        # If we are here, then there is no counter
        else:
            count = None

        return count

    @classmethod
    def flush_counter(cls, name):
        counter = cls.get_by_id(name)
        if not counter:
            counter = cls(id=name)

        # Get the current value
        value = memcache.get(name, cls._get_kind())

        # Store it to the counter
        counter.count = value

        if counter.count == 0:
            counter.key.delete()
        else:
            counter.put()

    @classmethod
    def incr(cls, name, value=1):
        """Increments the named counter.

        Args:
            name: The name of the counter.
            value: The value to increment by.
        """
        memcache.incr(name, value, cls._get_kind(), initial_value=0)
        cls.sched_flush(name)

    @classmethod
    def decr(cls, name, value=1):
        """Decrements the named counter.

        Args:
            name: The name of the counter.
            value: The value to increment by.
        """
        memcache.decr(name, value, cls._get_kind(), initial_value=0)
        cls.sched_flush(name)

    @classmethod
    def sched_flush(cls, name):
        """Tries to schedule a flush of the counter if there isn't any flush set"""
        interval_num = get_interval_number(datetime.datetime.now(), INTERVAL)
        task_name = '-'.join([str(el) for el in [cls._get_kind(), name, INTERVAL, interval_num]])
        try:
            deferred.defer(cls.flush_counter, name, _name=task_name,
                           _countdown=random.randint(0, INTERVAL))
        except (taskqueue.TaskAlreadyExistsError, taskqueue.TombstonedTaskError):
            pass

    @classmethod
    def get_trending(cls):
        """Returns top 4 trending tags"""
        return Tag.gql("ORDER BY count DESC LIMIT 5")

