/**
 * Created by konstantin on 29.03.2017.
 */

function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
           var cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
         }
      }
  }
  return cookieValue;
}

var csrftoken = getCookie('csrftoken');

$(document).ready(function () {
    var webSocket = new ReconnectingWebSocket('ws://' + window.location.host + '/room/',
        null, {maxReconnectAttempts:5, timeoutInterval:5000});

    webSocket.onmessage = function(message) {
        var data = JSON.parse(message.data);
        if (data.action == 'typing'){
            if ($('.messenger').data('user') != data.user)
            {
                $(".status--commenting").find('.typing-username').html(data.username);
                $(".status--commenting").addClass("visible");
                $(".status--commenting").css({'bottom': 0}); // update absolute position in div with overflow

                setTimeout(function () {
                    $(".status--commenting").removeClass("visible");
                }, 5000);
                $('.messenger__messages').animate({scrollTop: $('.messenger__messages').prop("scrollHeight")}, 1000);
            }
        }
        else{
            if (data.sender == $('.messenger').data('user'))
                $('.messenger__older-messages-toggle').find('.status--commenting').before(data.sender_message);
            else
                $('.messenger__older-messages-toggle').find('.status--commenting').before(data.recipient_message);

             $('.messenger__messages').animate({scrollTop: $('.messenger__messages').prop("scrollHeight")}, 1000);
        }
    };
    var can_typing = true;

    $('textarea').keyup(function (e) {
        var user = $('.messenger').data('user');
        if (can_typing == true){
            can_typing = false;

            $.ajax({
             url: $('.messenger').data('update'),
             data: {
                 user: user,
                 csrfmiddlewaretoken: csrftoken,
             },
             type: 'post',
             success: function (data) {
                 can_typing = true;
             }
         });
        }

    });

   $('.send_message').click(function (e) {
     var message = $(this).parents('.messenger__input').find('textarea').val();
     var sender = $(this).data('sender');
     var textarea = $(this).parents('.messenger__input').find('textarea');
     var send_button = $(this);

     if (message != '' && message != undefined) {
         send_button.attr('disabled', 'disabled');
         $.ajax({
             url: $(this).data('url'),
             data: {
                 message: message,
                 sender: sender,
                 csrfmiddlewaretoken: csrftoken,
             },
             type: 'post',
             success: function (data) {
                 textarea.val('');
                 send_button.removeAttr('disabled');
             }
         });
         e.preventDefault();
         e.stopPropagation();
     }
   });

});
