function ajax(method, url, data, successCallback)
{
    $.ajax({
        type: method,
        url: url,
        data: data,
        success: function(data) {
            if (successCallback) {
                successCallback(data);
            }
        }
    });
}