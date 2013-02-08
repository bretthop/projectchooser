# The following two methods generate JSON encoded responses.
# These work by decorating a resource method with either decoration,
# and then simply returning the entities to encode from the method.
#
# Decorate the resource method with @JsonSingleResult if you are only returning
# a single object.
#
# Decorate the resource method with @JsonListResult if you are returning a list
# of objects (this way even if you only return one object it will still be encoded as a list)
#
# Look in the resource package for examples

# TODO: Combine these into a single decorator called '@ProduceJson' that takes a string argument of either 'SINGLE' or 'LIST'
from app.util.Pson import Pson

def JsonSingleResult(func):
    def jsonSingleResult(self):
        pson = Pson()

        resource = func(self)

        pson.setAllowedFieldsString(self.request.get('filter'))

        self.response.headers = setResponseHeaders()
        self.response.out.write(pson.encodeModel(resource))

    return jsonSingleResult

def JsonListResult(func):
    def jsonListResult(self):
        pson = Pson()

        resources = func(self)

        pson.setAllowedFieldsString(self.request.get('filter'))

        self.response.headers = setResponseHeaders()
        self.response.out.write(pson.encodeModelList(resources))

    return jsonListResult

def setResponseHeaders():
    h = {'Content-Type': 'application/json', 'Pragma':'no-cache'}
    return h
