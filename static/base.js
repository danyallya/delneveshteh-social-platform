$(document).ready(function () {
    if (typeof likeUrl != "undefined")
        $(document).on('click', '.like-btn', function () {
            var objId = $(this).parent().find('.post-id').val();

            var $elem = $(this);

            if ($elem.hasClass('active')) {
                $elem.removeClass('active');
                $elem.html(parseInt($elem.html()) - 1);
            } else {
                $elem.addClass('active');
                $elem.html(parseInt($elem.html()) + 1);
            }

            $.ajax({
                type: 'POST',
                url: likeUrl,
                data: {
                    'post_id': objId
                },
                success: function (msg) {
                    var res = eval(msg);
                    var state = res.s;
                    var count = res.lc;

                    $elem.html("" + count);

                    if (state == 'on') {
                        $elem.addClass("active");
                    } else {
                        $elem.removeClass("active");
                    }

                }
            });
        });

});

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
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

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});
