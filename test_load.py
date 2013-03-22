"""A script which repeatedly posts new twisks to the backend"""
import datetime
import time
import random
import json


import requests

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

users = ("semion", "maxime", "sarah", "mina", "misha", "caroline", "maurice",
         "pauline")

sentence = 'The quick brown fox jumps over the lazy dog'

tags = [
    '#yolo',
    '#budget2013',
    '#yolo',
    '#testtag',
    '#yolo',
    '#yolo',
    '#somethingelse',
]

tag_source = "will display the definition of the word. However, most of\
the time, it does not come with example sentences of the English word, which\
will show you how to use the English word in sentences how to connect it with\
other words and with grammar structures. "

tags.extend(["#" + str(el) for el in tag_source.split(" ")])
while True:
    content = sentence + " " + " ".join(random.sample(tags, 5))

    req = requests.post(
        "http://localhost:8080/twisks/",
        data=json.dumps({"author": random.choice(users),
        "content": content}),
        headers=headers)

    print req.json()
    time.sleep(0.05)
