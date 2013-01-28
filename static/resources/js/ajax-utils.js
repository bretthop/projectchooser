DataType = {
    DEFAULT: 0,
    JSON: 1
};

ajax = (function() {
    var ajax = {};

    var _ajaxLoader = null;

    ajax.req = function(meth, url, data, dataType, doneCallback)
    {
        var contentType = 'application/x-www-form-urlencoded; charset=UTF-8'; // jQuery default

        if (dataType == DataType.JSON) {
            contentType = 'application/json';
            data = JSON.stringify(data);
        }

        $.ajax({
            type: meth,
            url: url,
            contentType: contentType,
            data: data
        })
            .done(function(data) {
                if (doneCallback) {
                    doneCallback(data);
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
            .removeClass('hidden')
            .addClass('visible');
    };

    ajax.hideAjaxLoader = function()
    {
        if (_ajaxLoader == null) {
            return;
        }

        $(_ajaxLoader)
            .removeClass('visible')
            .addClass('hidden');
    };

    return ajax;
})();