import string, base64, httpUtils

# Top secret
def createApiAuthenticationToken():
    sym = string.maketrans(
        "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz0123456789:",
        "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm9876543210:")

    secret = 'b2pJalM1Zk5kcGh5cVJVOVNmcE1FZFhQOGNuRDhPbm1hYWZEbFhucnFmcDo2UVE4NTJOMllVREVa\nREVXVUJZSE5NM1dR\n'
    secret = base64.decodestring(secret)
    sChunks = secret.split(':')

    username = string.translate(sChunks[1], sym)
    password = string.translate(sChunks[0], sym)

    return httpUtils.encodeAuth(username, password)