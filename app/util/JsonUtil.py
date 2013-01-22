from google.appengine.ext import db

import json

class JsonUtil:
    @staticmethod
    def simpleEncodeList(l):
        jsonString = ""

        for el in l:
            jsonString += JsonUtil.simpleEncodeObject(el) + ","

        return "[" + jsonString[0:len(jsonString)-1] + "]"

    @staticmethod
    def simpleEncodeObject(o):
        jsonStr = ""

        #TODO: throws 'dict' object has no attribute '__dict__' on Proposal.datastore_types.Key
        dic = o.__dict__

        for j, v in enumerate(dic):
            try:
                jsonProp = json.dumps({v: dic[v]})

                jsonStr += jsonProp[1:len(jsonProp)-1] + ","
            except TypeError:
                jsonStr += "\"" + str(v) + "\":"

                if isinstance(dic[v], list):
                    jsonStr += JsonUtil.simpleEncodeList(dic[v])
                else:
                    jsonStr += JsonUtil.simpleEncodeObject(dic[v])

                jsonStr += ","

        return "{" + jsonStr[0:len(jsonStr)-1] + "}"
