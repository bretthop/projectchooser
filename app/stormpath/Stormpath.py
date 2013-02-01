import urllib2, httpUtils, json, string, base64

def login(username, password):
    authInfo = getAPIAuthInfo()
    apiUrl = 'https://api.stormpath.com/v1/applications/Bhe5osLOQEe_oRnS7I-yEQ/loginAttempts'

    userData = {
        'type': 'basic',
        'value': httpUtils.encodeAuth(username, password)
    }

    request = urllib2.Request(apiUrl)

    request.add_header("Authorization", "Basic %s" % httpUtils.encodeAuth(authInfo['apiUser'], authInfo['apiPass']))
    request.add_header("Content-type", "application/json")

    try:
        # To get the response call the 'read()' function on the returned object:
        urllib2.urlopen(request, data = json.dumps(userData))

        return True
    except urllib2.URLError:
        return False

# TODO: Move to different python file
def getAPIAuthInfo():
    sym = string.maketrans(
        "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz0123456789:",
        "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm9876543210:")

    secret = 'b2pJalM1Zk5kcGh5cVJVOVNmcE1FZFhQOGNuRDhPbm1hYWZEbFhucnFmcDo2UVE4NTJOMllVREVa\nREVXVUJZSE5NM1dR\n'
    secret = base64.decodestring(secret)
    sChunks = secret.split(':')

    return {
        'apiUser': string.translate(sChunks[1], sym),
        'apiPass': string.translate(sChunks[0], sym)
    }
