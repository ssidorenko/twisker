import datetime
import time
import json

from google.appengine.ext import db

def query_to_json(query_obj):
    """Converts a gql query set, or a single model, respectively to JSON"""
    return GAEJSONEncoder().encode(query_obj)

class GAEJSONEncoder(json.JSONEncoder):
    """This json encoder parses models as dicts, with related models as id"""
    def default(self, o):
        # If it's a model, convert its properties to a dictionnary, which will
        # itself be parsed by the JSONEncoder later
        if isinstance(o, db.Model):
            output = {'id':o.key().id_or_name()}
            for key, prop in o.properties().iteritems():
                value = getattr(o,key) 
                if isinstance(value, db.Model):
                    value = value.key().id_or_name()
                elif isinstance(value, db.Key):
                    value = value.id_or_name()

                output[key] = value
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
