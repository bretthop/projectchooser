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
        resource = func(self)

        pson = Pson()
        expandStr = self.request.get('expand')

        if expandStr and not expandStr == '':
            pson.setAllowedFields(expandStr.split(','))

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(pson.encodeModel(resource))

    return jsonSingleResult

def JsonListResult(func):
    def jsonListResult(self):
        resources = func(self)

        pson = Pson()
        expandStr = self.request.get('expand')

        if expandStr and not expandStr == '':
            pson.setAllowedFields(expandStr.split(','))

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(pson.encodeModelList(resources))

    return jsonListResult