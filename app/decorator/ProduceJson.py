# The following method generates JSON encoded responses.
# These work by decorating a resource method with either decoration,
# and then simply returning the entities to encode from the method.
#
# Look in the resource package for examples

from app.util.Pson import Pson

def ProduceJson(func):
    def produceJson(self):
        pson = Pson()

        resource = func(self)

        pson.setAllowedFieldsString(self.request.get('filter'))

        self.response.headers = setResponseHeaders()
        self.response.out.write(pson.encodeModel(resource))

    return produceJson

def setResponseHeaders():
    h = {'Content-Type': 'application/json', 'Pragma':'no-cache'}
    return h
