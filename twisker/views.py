import logging
import json

from flask import Response, request
from jsonproc import json_query_view, GAEJSONEncoder

from google.appengine.ext import db

from twisker import app
from models import Twisk

@app.route('/twisks/', methods=['GET', 'POST'])
@json_query_view
def twisks():
    if request.method == 'GET':
        twisks = Twisk.gql("ORDER BY when DESC")
        return twisks
    elif request.method == 'POST':
        logging.debug(request.data)
        data = json.loads(request.data)

        twisk = Twisk(
            author=db.Key.from_path("TwiskUser", data['author']),
            content=data['content']
        )

        twisk.put()

        return twisk

@app.route('/twisks/<string:id>', methods=['GET','DELETE'])
@json_query_view
def get_twisk(id):
    twisk = Twisk.get_by_id(int(id))

    if request.method == 'DELETE':
        twisk.delete()
    else:
        return twisk.content
