import json, inspect
import collections
import datetime
from google.appengine.ext import db
from app.resources.RestApiResponse import RestApiResponse

class JsonUtil:
    # TODO: Turn this static Util class into a stateful object that has a list of processed objects ('done')
    # TODO: and a list of allowedFields ('allowedFields'). Then refactor till neat
    @staticmethod
    def encodeModelList(l, allowedFields = None):
        if not allowedFields:
            allowedFields = ['*.*']

        return json.dumps(JsonUtil._createJsonList(l, [], allowedFields))

    @staticmethod
    def encodeModel(m, allowedFields = None):
        if not allowedFields:
            allowedFields = ['*.*']

        return json.dumps(JsonUtil._createJsonObject(m, [], allowedFields))

    @staticmethod
    def _createJsonList(l, done, allowedFields):
        jsonList = []

        for el in l:
            jsonList.append(JsonUtil._createJsonObject(el, done[:], allowedFields))

        return jsonList

    @staticmethod
    def _createJsonObject(m, done, allowedFields):
        jsonObject = {}

        # If the Model is saved then update the 'id' field to contain the models proper id
        if hasattr(m, 'is_saved'):
            jsonObject = {'id': None}
            if m and m.is_saved():
                key = getattr(m, 'key')()

                jsonObject['id'] = key.id()
                done.append(key)

            for f, attr in JsonUtil._getJsonFields(m, done, allowedFields).iteritems():
                if isinstance(attr, (int, long, float, bool, dict, basestring)):
                    jsonObject[f] = attr
                elif isinstance(attr, datetime.date):
                    jsonObject[f] = str(attr) # TODO: Maybe add some date formatting here if needed
                elif isinstance(attr, db.GeoPt): # Added for no real reason
                    jsonObject[f] = {'lat': attr.lat, 'lon': attr.lon}
                elif isinstance(attr, collections.Iterable):
                    jsonObject[f] = JsonUtil._createJsonList(attr, done, allowedFields)
                else:
                    jsonObject[f] = JsonUtil._createJsonObject(attr, done, allowedFields)
        else:
            if isinstance(m, RestApiResponse):
                jsonObject['httpStatus'] = m._httpStatus
                jsonObject['urn']        = m._urn
                jsonObject['count']      = m._count
                jsonObject['user']       = JsonUtil._createJsonObject(m._user, done[:], allowedFields)
                jsonObject['items']      = JsonUtil._createJsonList(m._items, done[:], allowedFields)

        return jsonObject

    @staticmethod
    def _getJsonFields(model, done, allowedFields):
        def isPublicAttribute(name, value):
            return not (name.startswith('_') or inspect.ismethod(value) or inspect.isfunction(value))

        def isReverseReference(name):
            return name.endswith('_set')

        def isProcessed(done, value):
            if hasattr(value, 'key'):
                return getattr(value, 'key')() in done
            else:
                return False

        def isFieldAllowed(model, fieldName):
            className = type(model).__name__

            for allowedField in allowedFields:
                allowedClassName = allowedField.split('.')[0]
                allowedFieldName = allowedField.split('.')[1]

                if (className == allowedClassName or allowedClassName == '*') and (fieldName == allowedFieldName or allowedFieldName == '*'):
                    return True

            return False

        fields = {}

        for name, value in inspect.getmembers(model):
            if isFieldAllowed(model, name):
                if isPublicAttribute(name, value):
                    if not isReverseReference(name):
                        if not isProcessed(done, value):
                            fields[name] = value

        return fields

    @staticmethod
    def basicDecodeToModel(jsonStr, Model):
        jsonDict = json.loads(jsonStr)

        model = Model(**jsonDict)

        return model