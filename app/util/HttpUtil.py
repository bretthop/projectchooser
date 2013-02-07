import base64

def getAuthInfoFromHeader(request):
    authorisation = request.headers["Authorization"]

    return decodeAuth(authorisation.split('Basic ')[1])

def encodeAuth(username, password):
    return base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

def decodeAuth(base64Str):
    decoded = base64.decodestring(base64Str)

    return {
        'username': decoded.split(':')[0],
        'password': decoded.split(':')[1]
    }