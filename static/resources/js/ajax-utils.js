DataType = {
    DEFAULT: 0,
    JSON: 1
};

globalVars = (function() {
    var me = {};

    me.domainId = 0;

    /**
     * This describes the last request that was attempted to be made.
     * This request has failed due to the client not having any authentication information, and should be attempted
     * again once the user has entered there login details.
     */
    me.requestToRetry = undefined;

    return me;
})();

ajax = (function() {
    var ajax = {};

    var _ajaxLoader = null;

    ajax.req = function(params)
    {
        var url = params.url,
            authenticate = params.authenticate || true,
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
            if (session.hasUserCredentials()) {
                var authToken = session.getUserCredentialsAsAuthToken();

                ajaxDescriptor.beforeSend = function (xhr) { // TODO: See if you can set this by the 'headers' prop
                    xhr.setRequestHeader ('Authorization', 'Basic ' + authToken);
                };
            }
            else {
                ajax.hideAjaxLoader();
                globalVars.requestToRetry = params;
                showLoginModal();

                return;
            }
        }

        if (dataType && dataType == DataType.JSON) {
            ajaxDescriptor.contentType = 'application/json';
            ajaxDescriptor.data = JSON.stringify(data);
        }

        $.ajax(ajaxDescriptor)
            .done(function(data) {
                if (doneCallback) {
                    doneCallback(data);
                }
            })
            .fail(function(data) {
                if (failCallback) {
                    failCallback(data);
                }
            });
    };

    ajax.setAjaxLoader = function(loader)
    {
        _ajaxLoader = loader;
    };

    ajax.showAjaxLoader = function()
    {
        if (_ajaxLoader == null) {
            return;
        }

        $(_ajaxLoader)
            .removeClass('hidden');
    };

    ajax.hideAjaxLoader = function()
    {
        if (_ajaxLoader == null) {
            return;
        }

        $(_ajaxLoader)
            .addClass('hidden');
    };

    return ajax;
})();
