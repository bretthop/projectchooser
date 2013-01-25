from app.util.JsonUtil import *

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

def JsonSingleResult(func):
    def jsonSingleResult(self):
        resources = func(self)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(JsonUtil.encodeModel(resources))

    return jsonSingleResult

def JsonListResult(func):
    def jsonListResult(self):
        resources = func(self)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(JsonUtil.encodeModelList(resources))

    return jsonListResult