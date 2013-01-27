import json

class JsonUtil:
    @staticmethod
    def encodeModelList(l):
        jsonString = ""

        for el in l:
            jsonString += JsonUtil.encodeModel(el) + ","

        return "[" + jsonString[0:len(jsonString)-1] + "]"

    @staticmethod
    def encodeModel(m):
        jsonStr = ""

        # Try and get a list of fields to use in serialisation (this will fail if there is no 'jsonFields()' method
        # defined on the Model). If the Model has not defined this method (i.e. an exception occurs) then we will
        # ignore it currently (this behaviour may be changed in the future)
        try :
            fields = m.jsonFields()
        except BaseException:
            return 'null'

        # Try and insert the Model's ID (this will fail if the Mobile has not been saved yet)
        try:
            jsonStr += JsonUtil._encodeProperty('id', getattr(m, 'key')().id())
        except BaseException:
            pass

        # Loop through all fields and attempt to encode them
        for f in fields:
            attr = getattr(m, f)

            # Try and encode the attribute 'attr' for field 'f', if there is an error it means that 'attr' is a complex
            # object and we will need to encode it explicitly
            try:
                jsonProp = json.dumps({f: attr})

                jsonStr += jsonProp[1:len(jsonProp)-1] + ","
            except TypeError:
                # Try and get an iterator for the attribute, if it succeeds then 'attr' is a list object,
                # otherwise its a single object.
                # NOTE: This is obviously dirty, but apparently its the 'pythonic' way to do it, for now im leaving it as is
                #       but ill definitely change it
                try:
                    iter(attr)
                except TypeError: # attr is NOT a list
                    value = JsonUtil.encodeModel(attr)
                else: # attr is a list
                    value = JsonUtil.encodeModelList(attr)

                jsonStr += JsonUtil._encodeProperty(f, value)

        return "{" + jsonStr[0:len(jsonStr)-1] + "}"

    @staticmethod
    def _encodeProperty(name, value):
        return "\"%s\":%s," % (str(name), str(value))

    @staticmethod
    def decodeToDict(jsonStr):
        return json.loads(jsonStr)
