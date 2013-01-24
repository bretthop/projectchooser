DataType = {
    DEFAULT: 0,
    JSON: 1
};

function ajax(method, url, data, dataType, successCallback)
{
    var contentType = 'application/x-www-form-urlencoded; charset=UTF-8'; // JQuery default

    if (dataType == DataType.JSON) {
        contentType = 'application/json';
        data = JSON.stringify(data);
    }

    $.ajax({
        type: method,
        url: url,
        contentType: contentType,
        data: data
    })
    .done(function(data) {
        if (successCallback) {
            successCallback(data);
        }
    });
}