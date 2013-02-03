DataType = {
    DEFAULT: 0,
    JSON: 1
};

globalVars = (function() {
    var me = {};

    me.domainId = 0;

    return me;
})();

ajax = (function() {
    var ajax = {};

    var _ajaxLoader = null;

    ajax.req = function(meth, url, data, dataType, doneCallback, failCallback)
    {
        if (!session.hasUserCredentials()) {
            ajax.hideAjaxLoader();

            showLoginModal();

            return;
        }

        var contentType = 'application/x-www-form-urlencoded; charset=UTF-8'; // jQuery default

        if (dataType == DataType.JSON) {
            contentType = 'application/json';
            data = JSON.stringify(data);
        }

        $.ajax({
            type: meth,
            url: url,
            contentType: contentType,
            beforeSend: function (xhr) { // TODO: See if you can set this by the 'headers' prop
                // TODO: Generate auth token from session's username and password, this is a hardcoded token for (user = 'test@example.com', pass = 'Password1')
                xhr.setRequestHeader ('Authorization', 'Basic dGVzdEBleGFtcGxlLmNvbTpQYXNzd29yZDE=');
            },
            data: data
        })
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
