DataType = {
    DEFAULT: 0,
    JSON: 1
};

globalVars = (function() {
    var me = {};

    me.domainId = 0;

    /**
     * Holds a callback function that the login modal should call when the user
     * successfully logs in
     */
    me.loginCallback = undefined;

    return me;
})();

ajax = (function() {
    var ajax = {};

    var _ajaxLoaderSelector = null;

    ajax.req = function(params)
    {
        var url = params.url,
            authenticate = params.authenticate != undefined ? params.authenticate : true,
            email = params.email || (session.currentUser() && session.currentUser().email),
            password = params.password || (session.currentUser() && session.currentUser().password),
            method = params.method,
            data = params.data || '',
            dataType = params.dataType,
            doneCallback = params.doneCallback,
            failCallback = params.failCallback;

        var ajaxDescriptor = {
            url: url,
            type: method,
            data: data
        };

        if (authenticate) {
            if (email && password) {
                var authToken = base64.encode(email + ':' + password);

                ajaxDescriptor.beforeSend = function (xhr) { // TODO: See if you can set this by the 'headers' prop
                    xhr.setRequestHeader ('Authorization', 'Basic ' + authToken);
                };
            }
            else {
                ajax.hideAjaxLoader();

                globalVars.loginCallback = function() {
                    ajax.showAjaxLoader();
                    ajax.req(params);
                };

                showLoginModal();

                return;
            }
        }

        if (dataType && dataType == DataType.JSON) {
            ajaxDescriptor.contentType = 'application/json';
            ajaxDescriptor.data = JSON.stringify(data);
        }

        $.ajax(ajaxDescriptor)
            .done(function(response) {
                if (doneCallback) {
                    if (globalVars.debug) {
                        console.log('Retrieved ' + response.count + ' items with a ' + response.httpStatus + ' response code');
                    }

                    doneCallback(response.items);
                }
            })
            .fail(function(data) {
                if (failCallback) {
                    failCallback(data);
                }
            });
    };

    ajax.setAjaxLoaderSelector = function(loaderSelector)
    {
        _ajaxLoaderSelector = loaderSelector;
    };

    ajax.showAjaxLoader = function()
    {
        if (_ajaxLoaderSelector == null) {
            return;
        }

        $(_ajaxLoaderSelector)
            .removeClass('hidden');
    };

    ajax.hideAjaxLoader = function()
    {
        if (_ajaxLoaderSelector == null) {
            return;
        }

        $(_ajaxLoaderSelector)
            .addClass('hidden');
    };

    return ajax;
})();
