/**
 * Created by korablevop on 18.02.16.
 */





function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


$(document).ready(function(){

    var options = {autoplay: true,slidesToShow: 6,
                    slidesToScroll: 1,dots: true,speed: 600}

    $('.slider').slick(options);


    $("#nav-menu li").click(function() {
        $("#nav-menu li").removeClass("active"); //Удаление любого "active" класса
        $(this).addClass("active"); //Добавление "active" класса на категорию
        });

    $('#nav-menu a').each(function () {
        console.log(this.pathname)
        console.log(location.pathname)
    if (this.pathname == location.pathname) $(this).parent().addClass('active');
    }


    );



    //$('#form-comment').on('submit', function(event){
    //event.preventDefault();
    //console.log("form submitted!")  // sanity check
    ////create_post();
    //});

//    function create_post() {
//    console.log("create post is working!") // sanity check
//    $.ajax({
//        url : "/comments/post/", // the endpoint
//        type : "POST", // http method
//        data : { 'the_post' : $('#id_comment').val(),
//
//                 'object_pk' :  $('#id_object_pk').val(),
//                 'id_content_type' :  $('#id_content_type').val(),
//                 'csrfmiddlewaretoken':getCookie('csrftoken'),
//        }, // data sent with the post request
//
//        // handle a successful response
//        success : function(json) {
//            $('#id_comment').val(''); // remove the value from the input
//            console.log(json); // log the returned json to the console
//            console.log("success"); // another sanity check
//        },
//
//        // handle a non-successful response
//        error : function(xhr,errmsg,err) {
//            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
//                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
//            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
//        }
//    });
//};

$('.category').click(function(){

        console.log('Нажал');


});


});








$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

function show_reply_form(event) {
            var $this = $(this);
            var comment_id = $this.data('comment-id');

            $('#id_parent').val(comment_id);
            $('#form-comment').insertAfter($this.closest('.comment'));
        };

function cancel_reply_form(event) {
            $('#id_comment').val('');
            $('#id_parent').val('');
            $('#form-comment').appendTo($('#wrap_write_comment'));
        }

$.fn.ready(function() {
            $('.comment_reply_link').click(show_reply_form);
            $('#cancel_reply').click(cancel_reply_form);
        })