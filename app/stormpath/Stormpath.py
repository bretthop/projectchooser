import httpUtils

API_BASE_URL = 'https://api.stormpath.com/v1/'
API_LOGIN_URL = API_BASE_URL + 'applications/%s/loginAttempts'

APPLICATION_ID = 'Bhe5osLOQEe_oRnS7I-yEQ'

def login(username, password):
    loginUrl = API_LOGIN_URL % APPLICATION_ID

    loginData = {
        'type': 'basic',
        'value': httpUtils.encodeAuth(username, password)
    }

    loginResult = httpUtils.post(loginUrl, loginData)

    return loginResult