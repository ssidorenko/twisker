from google.appengine.ext import ndb


class TwiskUser(ndb.Model):
    followers = ndb.KeyProperty(kind='TwiskUser', repeated=True)
    following = ndb.KeyProperty(kind='TwiskUser', repeated=True)

    tags = ndb.StringProperty(repeated=True)

    # TODO find another way to realise this without hitting the 5 write/s limit
    @ndb.transactional(xg=True)
    def follow(self, other_username):
        other_user = TwiskUser.get_by_id(other_username)

        if other_user.key() != self.key() and other_user.key() not in self.following:
            other_user.followers.append(self.key())
            self.following.append(other_user.key())
            other_user.put()
            self.put()

    def _pre_put_hook(self):
        self.parse_tags()

    def parse_tags(self):
        for word in self.content.split(" "):
            if word[0] == '#':
                self.add_tag(word)

    def add_tag(self):
        pass


class Twisk(ndb.Model):
    content = ndb.StringProperty(required=True)
    when = ndb.DateTimeProperty(auto_now_add=True)
    author = ndb.KeyProperty(kind='TwiskUser')
