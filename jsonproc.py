import datetime
import time
import json
from functools import wraps

from flask import Response

from google.appengine.ext import db

class GAEJSONEncoder(json.JSONEncoder):
    """This json encoder parses models as dicts, with related models as id"""
    def default(self, o):
        # If it's a model, convert its properties to a dictionnary, which will
        # itself be parsed by the JSONEncoder later
        if isinstance(o, db.Model):
            output = {}
            for key, prop in o.properties().iteritems():
                value = getattr(o,key) 
                if isinstance(value, db.Model):
                    value = str(value.key().id_or_name())
                elif isinstance(value, db.Key):
                    value = value.id_or_name()

                output[key] = value
                
            output['id'] = str(o.key().id_or_name())
            return output
        elif isinstance(o, db.Query) or isinstance(o, db.GqlQuery):
            return list(o)
        elif isinstance(o, db.GeoPt):
            return {'lat': o.lat, 'lon': o.lon}
        elif isinstance(o, db.Key):
            return o.id_or_name()
        elif isinstance(o, datetime.date):
            # Convert date/datetime to ms-since-epoch ("new Date()").
            ms = time.mktime(o.utctimetuple())
            ms += getattr(o, 'microseconds', 0) / 1000
            return int(ms)
        else:
            raise ValueError('cannot encode ' + repr(o))

def json_query_view(f):
    """Small decorators that runs the output of the passed function through the
    json serializer and through a flask json response"""
    @wraps(f)
    def decorated(*args, **kwargs):
        return json_response(
            GAEJSONEncoder().encode(
                f(*args, **kwargs)
            )
        )

    return decorated

def json_response(data):
    """Return a Flask response with JSON mimetype"""
    resp = Response(data, status=200, mimetype='application/json')
    return resp
