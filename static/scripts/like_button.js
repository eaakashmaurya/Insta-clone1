$('.like_toggle_button').click(function(){
    var id;
    id = $(this).attr("data-post-id");
    // console.log(id);
    $.ajax({
        type: "POST",
        url: "like",
        data: {post_id: id},
        success: function( data ) {
            $( '#like_cnt'+id ).text(data.likes_cnt);
            console.log($( '#like'+id ).children().first());
            if (data.like_status == 1) {
                // alert("Liked");
                $( '#like'+id ).children().first().attr('class', 'fas fa-heart');
            }
            else {
                // alert("Unliked");
                $( '#like'+id ).children().first().attr('class', 'far fa-heart');
            }
        }
    })
})