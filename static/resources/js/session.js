session = (function() {
    var sesh = {};

    sesh.getUserCredentials = function()
    {
        return {
            email: sessionStorage.getItem('email'),
            password: sessionStorage.getItem('password')
        }
    };

    sesh.setUserCredentials = function(email, password)
    {
        sessionStorage.setItem('email', email);
        sessionStorage.setItem('password', password);
    };

    sesh.hasUserCredentials = function()
    {
        var userCredentials = sesh.getUserCredentials();

        return userCredentials && userCredentials.email != undefined && userCredentials.password != undefined;
    };

    sesh.clearUserCredentials = function()
    {
        sessionStorage.removeItem('email');
        sessionStorage.removeItem('password');
    };

    return sesh;
})();