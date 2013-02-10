import collections

class RestApiResponse():

    _httpStatus = ''
    _urn        = ''
    _count      = 0
    _items      = []

    @staticmethod
    def init(statusCode, items = None):
        result = RestApiResponse()
        result._httpStatus = statusCode

        # Look Before You Leap
        # There can be three cases for 'items': 1) None, 2) a single Model object, 3) a GqlQuery representing a list of Models
        if not items:
            result._items = []
            result._count = 0
        elif not isinstance(items, collections.Iterable):
            result._items = [items]
            result._count = len(result._items)
        else:
            result._items = items
            result._count = items.count()

        return result