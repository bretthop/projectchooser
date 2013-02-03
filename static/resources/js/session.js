session = (function() {
    var sesh = {};

    sesh.getUserCredentials = function()
    {
        return {
            username: sessionStorage.getItem('username'),
            password: sessionStorage.getItem('password')
        }
    };

    sesh.getUserCredentialsAsAuthToken = function ()
    {
        if (!sesh.hasUserCredentials()) {
            return undefined;
        }

        var credentials = sesh.getUserCredentials();

        return base64.encode(credentials.username + ':' + credentials.password);
    };

    sesh.setUserCredentials = function(username, password)
    {
        sessionStorage.setItem('username', username);
        sessionStorage.setItem('password', password);
    };

    sesh.hasUserCredentials = function()
    {
        var userCredentials = sesh.getUserCredentials();

        return userCredentials && userCredentials.username != undefined && userCredentials.password != undefined;
    };

    sesh.clearUserCredentials = function()
    {
        sessionStorage.removeItem('username');
        sessionStorage.removeItem('password');
    };

    return sesh;
})();