$(document).ready(function () {

    $('.login').click(function () {
        $("#login-box").fadeIn();
    });

    $('.signup').click(function () {
        $("#signup-box").fadeIn();
    });

    $('.go-signup').click(function () {
        $(this).parents('.account-section').fadeOut(function () {
            $("#signup-box").fadeIn();
        });
    });

    // AUTH CHECK
    $(document).on('click', '.login-need', function (e) {
        if (!is_auth) {
            $("#login-box").fadeIn();
            e.preventDefault();
            e.stopPropagation();
        }
    });

    $(document).on('click', '.signup-need', function (e) {
        if (!is_auth) {
            $("#signup-box").fadeIn();
            e.preventDefault();
            e.stopPropagation();
        }
    });

    $('#signup-box .submit').click(function (e) {
        $('#signup-name + div').html("");
        $('#signup-pass + div').html("");

        var name = $('#signup-name').val();
        var password = $('#signup-pass').val();
        var flag = true;
        if (!password || password.length < 4) {
            $('#signup-pass + div').html("رمز عبور حداقل باید 4 حرف باشد.");
            flag = false;
        }

        if (flag) {
            $.ajax({
                type: 'POST',
                url: checkSignupUrl,
                data: {
                    'username': name
                },
                success: function (msg) {
                    var res = eval(msg);

                    if (res) {
                        $('#signup-box form').submit();
                    } else {
                        $('#signup-name + div').html("نام کاربری تکراری است.");

                    }
                }
            });
        }

        e.preventDefault();
        return false;
    });

    $('#login-box .submit').click(function (e) {

        var username = $('#login-username').val();
        var password = $('#login-pass').val();

        $('#login-box .message').html("");

        $.ajax({
            type: 'POST',
            url: checkUrl,
            data: {
                'username': username,
                'password': password
            },
            success: function (msg) {
                var res = eval(msg);

                if (res) {
                    $('#login-box form').submit();
                } else {
                    $('#login-box .message').html("نام کاربری یا رمز عبور اشتباه است.");
                }

            }
        });

        e.preventDefault();
        return false;

    });


    if (typeof likeUrl != "undefined")
        $(document).on('click', '.like-btn', function () {

            if (!is_auth)
                return;

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


    // POST PAGe


    if (typeof sendCommentUrl != "undefined")
        $(document).on('click', '.share-btn', function () {
            var objId = $('#obj_id').val();
            var text = $('.share-input').val();

            if (text)
                $.ajax({
                    type: 'POST',
                    url: sendCommentUrl,
                    data: {
                        'obj_id': objId,
                        'text': text
                    },
                    success: function (msg) {
                        var res = eval(msg);
                        var content = res.content;
                        var count = res.count;

                        $('#comments-container').prepend(content);
                        $('.share-input').val("");

                        alertify.success("نظر شما با موفقیت ثبت شد.");

                        //$('.comments-count').html(count);

                        //$('.comment').removeClass("hidden-only");

                        //$('.Banner').remove();
                    }
                });
            $('.Share').removeClass("active");

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
