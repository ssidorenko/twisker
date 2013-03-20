from twisker import app
from models import Twisk
from flask import Response
from jsonproc import query_to_json

@app.route('/twisks')
def list_twisks():
    twisks = Twisk.gql("ORDER BY when DESC")

    return json_response(query_to_json(twisks))

@app.route('/twisk/<int:id>')
def get_twisk(id):
    Twisk.get_by_id(id).content

def json_response(data):
    """Return a Flask response with JSON mimetype"""
    resp = Response(data, status=200, mimetype='application/json')
    print data
    return resp
