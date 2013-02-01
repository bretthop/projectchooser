import base64

def encodeAuth(username, password):
    return base64.encodestring('%s:%s' % (username, password)).replace('\n', '')