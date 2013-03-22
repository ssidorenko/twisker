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
    '#yolo'
    '#somethingelse',
]

while True:
    content = sentence + " " + " ".join(random.sample(tags, 2)) + \
        " " + str(datetime.datetime.now())

    req = requests.post(
        "http://localhost:8080/twisks/",
        data=json.dumps({"author": random.choice(users),
        "content": content}),
        headers=headers)

    print req.json()
    time.sleep(0.005)
