function get_quote(destElem) {
    $(destElem).html(`<img src=${loadingFilename}>`);
    $.get('/get_quote').done(function(response) {
        $(destElem).text(response['quote'])
    }).fail(function(error) {
        $(destElem).text(error);
    });
}