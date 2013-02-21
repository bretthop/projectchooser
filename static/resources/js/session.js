session = (function() {
    var sesh = {};

    sesh.setUser = function(user, password)
    {
        if (!user) {
            console.log('A user has been set into the session without a username!');
        }

        if (!password) {
            console.log('A user has been set into the session without a password!');
        }

        // TODO: Store the base64 representation of the password, instead of the actual password
        user.password = password;

        sessionStorage.setItem('user', JSON.stringify(user));
    };

    sesh.currentUser = function()
    {
        var jsonUser = sessionStorage.getItem('user');

        var user = JSON.parse(jsonUser);

        if (user) {
            // This does not seem like an appropriate place to have this method, but the SessionStorage cannot store objects
            // Which makes it difficult to store objects with functions.
            // TODO: Implement a generic way of storing objects (with functions) in the session
            user.hasPermission = function(permissionName)
            {
                var hasPermission = false;

                _.each(this.role.permissions, function(permission) {
                    if (permission.name == permissionName) {
                        hasPermission = true;
                    }
                });

                return hasPermission;
            };
        }

        return user;
    };

    sesh.isUserLoggedIn = function()
    {
        return sesh.currentUser() != null;
    };

    sesh.clearUser = function()
    {
        sessionStorage.removeItem('user');
    };

    return sesh;
})();