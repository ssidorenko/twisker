"REST API to post and retrieve twisks"
import logging
import json

from flask import request, abort, Blueprint
from jsonproc import json_query_view
from google.appengine.ext import ndb

from models import Twisk

api = Blueprint('api', __name__)


@api.route('/twisks/', methods=['GET', 'POST'])
@json_query_view
def twisks():
    """Returns all twisks in JSON format. All of them."""
    if request.method == 'GET':
        twisks = Twisk.gql("ORDER BY when DESC LIMIT 20")
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


@api.route('/twisks/<string:id>', methods=['GET', 'DELETE'])
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


@api.route('/twisks/tagged/<string:tag>', methods=['GET'])
@json_query_view
def get_tag(tag):
    """Returns all twisks tagged with a given tag"""
    twisks = Twisk.gql("WHERE tags = :1 ORDER BY when DESC", tag)
    return twisks
