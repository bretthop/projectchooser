import json, inspect
import collections
import datetime
from google.appengine.ext import db
from app.resources.RestApiResponse import RestApiResponse

class JsonUtil:

    @staticmethod
    def encodeModelList(l):
        return json.dumps(JsonUtil._createJsonList(l, []))

    @staticmethod
    def encodeModel(m):
        return json.dumps(JsonUtil._createJsonObject(m, []))

    @staticmethod
    def _createJsonList(l, done):
        jsonList = []

        for el in l:
            jsonList.append(JsonUtil._createJsonObject(el, done[:]))

        return jsonList

    @staticmethod
    def _createJsonObject(m, done):
        jsonObject = {}

        # If the Model is saved then update the 'id' field to contain the models proper id
        if hasattr(m, 'is_saved'):
            jsonObject = {'id': None}
            if m and m.is_saved():
                key = getattr(m, 'key')()

                jsonObject['id'] = key.id()
                done.append(key)

            for f, attr in JsonUtil._getJsonFields(m, done).iteritems():
                if isinstance(attr, (int, long, float, bool, dict, basestring)):
                    jsonObject[f] = attr
                elif isinstance(attr, datetime.date):
                    jsonObject[f] = str(attr) # TODO: Maybe add some date formatting here if needed
                elif isinstance(attr, db.GeoPt): # Added for no real reason
                    jsonObject[f] = {'lat': attr.lat, 'lon': attr.lon}
                elif isinstance(attr, collections.Iterable):
                    jsonObject[f] = JsonUtil._createJsonList(attr, done)
                else:
                    jsonObject[f] = JsonUtil._createJsonObject(attr, done)
        else:
            if isinstance(m, RestApiResponse):
                jsonObject['httpStatus'] = m._httpStatus
                jsonObject['urn']        = m._urn
                jsonObject['count']      = m._count
                jsonObject['user']       = JsonUtil._createJsonObject(m._user, done)
                jsonObject['items']      = JsonUtil._createJsonList(m._items, done)

        return jsonObject

    @staticmethod
    def _getJsonFields(model, done):
        def isPublicAttribute(name, value):
            return not (name.startswith('_') or inspect.ismethod(value) or inspect.isfunction(value))

        def isReverseReference(name):
            return name.endswith('_set')

        def isProcessed(done, value):
            if hasattr(value, 'key'):
                return getattr(value, 'key')() in done
            else:
                return False

        fields = {}

        for name, value in inspect.getmembers(model):
            if isPublicAttribute(name, value):
                if not isReverseReference(name):
                    if not isProcessed(done, value):
                        fields[name] = value

        return fields

    @staticmethod
    def decodeToModel(jsonStr, Model):
        jsonDict = json.loads(jsonStr)

        model = Model()

        for name, value in jsonDict.iteritems():
            setattr(model, name, value)

        return model