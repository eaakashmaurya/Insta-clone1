function searchOpen() {
    var search = $('#txtSearch').val()
    var data = {
        search: search
    };
    $.ajax({
        type: "GET",
        url: '/search.json',
        data: data,
        dataType: 'jsonp',
        jsonp: 'callback',
        jsonpCallback: 'searchResult'
    });
}


function searchResult(data) {
    $( "#txtSearch" ).autocomplete ({
        source: data
    });
}