import base64, urllib2, json
from secret import *


# This file contains some generic methods to deal with sending HTTP requests.
#
# It has been somewhat tailored to suit Stormpath, as each get, post, put, etc method automatically
# inserts the Stormpath API username/password authentication

def post(url, data):
    '''
        Performs a POST request to the given URL with the given data.

        The data is JSON serialised and sent in the body of the request.

        The response is JSON deserialised and returned back to the caller.
    '''
    request = urllib2.Request(url)

    request.add_header("Authorization", "Basic %s" % createApiAuthenticationToken())
    request.add_header("Content-type", "application/json")

    try:
        resp = urllib2.urlopen(request, data = json.dumps(data))

        jsonResp = json.loads(resp.read())
    except BaseException as e:
        jsonResp = None # TODO: Add proper error handling

    return jsonResp

def encodeAuth(username, password):
    return base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

def decodeAuth(base64Str):
    decoded = base64.decodestring(base64Str)

    return {
        'username': decoded.split(':')[0],
        'password': decoded.split(':')[1]
    }
