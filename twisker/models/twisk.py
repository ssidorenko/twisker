import logging
from google.appengine.ext import ndb
from tag import Tag


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
