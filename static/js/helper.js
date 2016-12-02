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

    var frm = $('#set_bet_form');

frm.submit(function(){

            //console.log("Submit form");
            //console.log($("#inn").val());

        if($("#inn").val() == '')

                {

                    alert('Ставка не может быть пустой');

                    return false;

                }

        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            //data:  frm.serialize(), /// doesn't work

            data:{
                'bet': $('#inn').val(),
                'auct_id': $('#auct_id').val(),
                'user_id': $('#user_id').val(),

                'csrfmiddlewaretoken':getCookie('csrftoken') }, //work
            success: function (data) {

                if (data['error']) {
                    $('#error').show()
                    $("#error").html(data['error']);
                    setTimeout(function(){$('#error').hide()},3000);  //30000 = 30 секунд

                    }
                else {

                    console.log(data['min_bet']);
                    $("#mess").html(data['bet']);
                    $("#inn").val(data['min_bet']);
                    $("#inn").attr('min',data['min_bet']);

                }

            },
            error: function(data) {
                $("#error").html("Something went wrong!");
            }
        });
        return false;


});


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

$("#nav-menu li").click(function() {
        $("#nav-menu li").removeClass("active"); //Удаление любого "active" класса
        $(this).addClass("active"); //Добавление "active" класса на категорию
        });

    $('#nav-menu a').each(function () {
        //console.log(this.pathname)
        //console.log(location.pathname)
    if (this.pathname == location.pathname) $(this).parent().addClass('active');
    }


    );


});



function getParameterByName(name, url) {
    if (!url) {
      url = window.location.href;
    }
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}



function get_attr_form(subcategory_id)
{
        $.ajax({
            url: "/callboard/get_attribute_form/" + subcategory_id+ "/yes/",
            type: "GET",
            //data: {subcategory_id: subcategory_id},
            success: function(response) {

              // response is form in html format

              div = '<div class="formdiv"></div>';
              console.log(response)
              $("#id_name").after(div);
              $(".formdiv").html(response);

            }
        })
  }



function get_subcat_list(category_id)
{
        $.ajax({
            url: "/callboard/get_subcategory_list/" + category_id,
            type: "GET",
            //data: {subcategory_id: subcategory_id},
            success: function(data) {

              // response is form in html format


              console.log(data);

              $(".subcatdiv").html(data);

            }
        })
}


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