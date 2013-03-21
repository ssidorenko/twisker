import logging
import json

from flask import request, abort
from jsonproc import json_query_view
from google.appengine.ext import ndb

from twisker import app
from models import Twisk


@app.route('/twisks/', methods=['GET', 'POST'])
@json_query_view
def twisks():
    """Returns all twisks in JSON format. All of them."""
    if request.method == 'GET':
        twisks = Twisk.gql("ORDER BY when DESC")
        return twisks
    elif request.method == 'POST':
        logging.debug(request.data)
        data = json.loads(request.data)

        twisk = Twisk(
            author=ndb.Key("TwiskUser", data['author']),
            content=data['content']
        )

        twisk.put()

        return twisk


@app.route('/twisks/<string:id>', methods=['GET', 'DELETE'])
@json_query_view
def get_twisk(id):
    """Returns a single twisk, also accept DELETE"""
    twisk = Twisk.get_by_id(int(id))

    if not twisk:
        abort(404)

    if request.method == 'DELETE':
        twisk.delete()
    else:
        return twisk.content


@app.route('/twisks/tagged/<string:tag>', methods=['GET'])
@json_query_view
def get_tag(tag):
    """Returns all twisks tagged with a given tag"""
    twisks = Twisk.gql("WHERE tags = :1 ORDER BY when DESC", tag)
    return twisks