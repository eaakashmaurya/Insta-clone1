$('.follow_toggle_button').click(function(){
    var id;
    id = $(this).attr("data-user-id");
    // console.log(id);
    $.ajax({
        type: "POST",
        url: "../follow",
        data: {user_id: id},
        success: function( data ) {
            // alert(data.followers_cnt);
            $(".follow_toggle_button").text(data.follow_button_status);
            $(".followers").text(data.followers_cnt);
        }
    })
})