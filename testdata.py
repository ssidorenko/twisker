"""Generate some test user and twisks"""

import random

from twisker.models import TwiskUser, Twisk

test_users = ("semion", "maxime", "sarah", "mina", "misha", "caroline", "maurice",
              "pauline")

sentence = 'The quick brown fox jumps over the lazy dog'

tags = [
    '#yolo',
    '#budget2013',
    '#yolo',
    '#testtag',
    '#yolo',
    '#yolo'
    '#somethingelse',
]

# use each username, reversed, as a hashtag
tags.extend(['#' + el[::-1] for el in test_users])


for i, u in enumerate(test_users):
    twisk_user = TwiskUser.get_or_insert(u)
    twisk_user.put()

    for j in xrange(90):
        content = sentence + " " + ", ".join(random.sample(tags, 2))

        Twisk(author=twisk_user.key, content=content).put()

    for other_user in test_users[:i]:
        print 1, u, other_user
        twisk_user.follow(other_user)


