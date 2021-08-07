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
        source: data,
        appendTo: "#searchbar",
        select: function() {
            // var user_to_search = $('#txtSearch').val();
            var user_to_search = $('.ui-state-focus:first').text();
            console.log($('.ui-state-focus:first').text());
            window.location.href = "/users/"+user_to_search;
        }
    });
}