"""Generate some test user and twisks"""

import random
import string

from twisker.models import TwiskUser, Twisk

test_users = ("semion", "maxime", "sarah", "mina", "misha", "caroline", "maurice",
"pauline")

sentence = 'The quick brown fox jumps over the lazy dog'


for i, u in enumerate(test_users):
    twisk_user  = TwiskUser.get_or_insert(key_name=u)
    twisk_user.put()
    
    for j in xrange(15):
        content = "".join( [random.choice(string.letters) for j in xrange(15)] )
        Twisk(author=twisk_user,content=content).put()

    for other_user in test_users[:i]:
        print 1, u, other_user
        twisk_user.follow(other_user)
    

