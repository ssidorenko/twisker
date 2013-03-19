def query_to_json(query_obj):
    """Converts a gql query set, or a single model, respectively to JSON"""

def query_to_data(query_obj):
    """Converts a gql query set, or a single model, respectively to a list
    of dict or a dict"""

    # Iterates only if we're processing a query or list of items
    if hasattr(query_obj, "__iter__"):
        result = []
        for entry in query_obj:
            result.append(
                to_dict(entry)
            )
        return result
    else:
        return to_dict(query_obj)

def to_dict(model):
    """Converts a GAE model instance to a dictionnary"""
    output = {}

    for key, prop in model.properties().iteritems():
        value = getattr(model, key)

        if value is None or isinstance(value, SIMPLE_TYPES):
            output[key] = value
        elif isinstance(value, datetime.date):
            # Convert date/datetime to ms-since-epoch ("new Date()").
            ms = time.mktime(value.utctimetuple())
            ms += getattr(value, 'microseconds', 0) / 1000
            output[key] = int(ms)
        elif isinstance(value, db.GeoPt):
            output[key] = {'lat': value.lat, 'lon': value.lon}
        elif isinstance(value, db.Model):
            output[key] = to_dict(value)
        elif isinstance(value, users.User):
            output[key] = value.user_id()
        else:
            raise ValueError('cannot encode ' + repr(prop))
    output["id"] = str(model.key().id_or_name())

    return output
