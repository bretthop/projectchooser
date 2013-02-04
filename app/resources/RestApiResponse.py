
class RestApiResponse():

    _httpStatus = ''
    _urn        = ''
    _count      = 0
    _items      = []

    @staticmethod
    def init(statusCode, items):
        result = RestApiResponse()
        result._httpStatus = statusCode
        result._items      = items
        result._count      = items.count()

        return result