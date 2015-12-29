import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import striptags
from django.utils.encoding import smart_text

from account.forms import SignUpFormNoCaptcha, ProfileForm
from account.models import Profile, Suggestion
from comment.handler import CommentHandler
from comment.models import Comment, LikeComment
from favorites.models import Favorite
from post.models import Post, PostContentType, PostReport, PostLike
from utils.calverter import gregorian_to_jalali
from utils.messages import MessageServices


def logout(request):
    from django.contrib.auth import logout

    logout(request)
    response = HttpResponse(json.dumps(get_auth_values(request)), 'application/json')
    return response


def login(request):
    from django.contrib.auth import authenticate, login

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        # remember = request.POST.get('remember')
        # if remember in [2, '2']:
        #     request.session.set_expiry(None)

        user = authenticate(username=username, password=password)
        if user is None or not user.is_active:
            message = u"نام کاربری یا گذرواژه نادرست است."
            # print {'m': message, 'login': False}
            return HttpResponse(json.dumps({'m': message, 'login': False}),
                                'application/json')
        else:
            login(request, user)
            # print get_auth_values(request)
            check_user(request)
            return HttpResponse(json.dumps(get_auth_values(request)),
                                'application/json')
    else:
        return initial_post(request)


def signup(request):
    if request.method == 'POST':
        post = request.POST.copy()
        form = SignUpFormNoCaptcha(post)
        if form.is_valid():
            form.save()
            data = get_auth_values(request)
            data.update({'success': True})
            return HttpResponse(json.dumps(data), 'application/json')
        else:
            message = ""
            for error in form.errors:
                message += striptags(form.fields[error].label) + u": " + striptags(form.errors[error]) + u"\n"
            data = get_auth_values(request)
            data.update({'success': False, 'm': message})
            response = HttpResponse(json.dumps(data), 'application/json')
            return append_csrf(request, response)
    else:
        return initial_post(request)


@login_required
def edit_profile(request):
    check_user(request)
    if request.method == 'POST':
        profile = request.user
        post = request.POST.copy()
        form = ProfileForm(post, instance=profile)
        if form.is_valid():
            user = form.save()
            data = get_auth_values(request)
            data.update({'success': True, 'user': profile.get_android_fields()})
            return HttpResponse(json.dumps(data), 'application/json')
        else:
            message = ""
            for error in form.errors:
                message += striptags(form.fields[error].label) + u": " + striptags(form.errors[error]) + u"\n"
            data = get_auth_values(request)
            data.update({'success': False, 'm': message})
            response = HttpResponse(json.dumps(data), 'application/json')
            return append_csrf(request, response)
    else:
        return initial_post(request)


def last_post_count(request, last_id):
    check_user(request)
    if not last_id or last_id == 0:
        last_id = 99999999

    count = Post.objects.filter(active=True, id__gt=last_id).count()

    return HttpResponse(json.dumps({'c': count}), 'application/json')


def post_list(request):
    check_user(request)
    p = request.GET.get('p')

    if p == 'popular':
        posts_obj = Post.objects.filter(active=True, like_count__gt=0).order_by('-like_count')[:20]
    elif p == 'favs':
        if request.user.is_anonymous():
            posts_obj = Post.objects.none()
        else:
            posts_obj = Post.objects.filter(active=True, likes__user=request.user).order_by('-id')
    else:
        posts_obj = Post.objects.filter(active=True).order_by('-id')[:5]

    return HttpResponse(Post.get_old_summery_json(posts_obj, request.user), 'application/json')


def last_post_list(request, last_id):
    check_user(request)
    if not last_id or last_id == 0:
        last_id = 99999999

    posts_obj = Post.objects.filter(active=True, id__gt=last_id).order_by('-id')[:5]

    return HttpResponse(Post.get_old_summery_json(posts_obj, request.user), 'application/json')


def next_post_list(request, first_id):
    check_user(request)
    if not first_id or first_id == -1:
        first_id = 0

    posts_obj = Post.objects.filter(active=True, id__lt=first_id).order_by('-id')[:5]

    return HttpResponse(Post.get_old_summery_json(posts_obj, request.user), 'application/json')


def user_post_list(request):
    check_user(request)
    username = request.GET.get('u')
    posts_obj = Post.objects.filter(active=True, creator__username=username).order_by('-id')[:5]

    return HttpResponse(Post.get_summery_json(posts_obj, request.user), 'application/json')


def user_last_post_list(request, last_id):
    check_user(request)
    username = request.GET.get('u')
    if not last_id or last_id == 0:
        last_id = 99999999

    posts_obj = Post.objects.filter(active=True, id__gt=last_id, creator__username=username).order_by('-id')[:5]

    return HttpResponse(Post.get_summery_json(posts_obj, request.user), 'application/json')


def user_next_post_list(request, first_id):
    check_user(request)
    username = request.GET.get('u')
    if not first_id or first_id == -1:
        first_id = 0

    posts_obj = Post.objects.filter(active=True, id__lt=first_id, creator__username=username).order_by('-id')[:5]

    return HttpResponse(Post.get_summery_json(posts_obj, request.user), 'application/json')


def user_posts(request):
    check_user(request)

    username = request.GET.get('u')
    first_id = request.GET.get('f')
    last_id = request.GET.get('l')

    posts_obj = Post.objects.filter(active=True)

    if username:
        user = get_object_or_404(Profile, username=username)
        posts_obj = posts_obj.filter(creator__username=username)

    if first_id:
        posts_obj = posts_obj.filter(id__lt=first_id)

    if last_id:
        posts_obj = posts_obj.filter(id__gt=last_id)

    posts_obj = posts_obj.distinct().order_by('-id')[:5]

    data = []
    for post in posts_obj:
        data.append(post.get_summery_fields(request.user))

    res = {'d': data}

    if username:
        res.update(user.get_user_summery())

    return HttpResponse(json.dumps(res), 'application/json')


@login_required
def send_post(request):
    check_user(request)
    if request.method == 'POST':
        text = striptags(request.POST.get('text')).strip().replace(
            "/[\u2190-\u21FF]|[\u2600-\u26FF]|[\u2700-\u27BF]|[\u3000-\u303F]|[\u1F300-\u1F64F]|[\u1F680-\u1F6FF]/g",
            "")
        if text:
            post = Post(
                text=text,
                creator=request.user if request.user.is_authenticated() else None,
                name=request.user.username
            )

            p = request.POST.get('p')
            v = request.POST.get('v')
            a = request.POST.get('a')

            if p:
                post.post_type = Post.get_post_type_by_param(p)

            if v:
                try:
                    v = int(v)
                    post.version_code = v
                except:
                    pass

            if a:
                try:
                    a = int(a)
                    post.android_version = a
                except:
                    pass

            post.save()

            data = get_auth_values(request)
            data.update({'success': True})

            return HttpResponse(json.dumps(data), 'application/json')
        else:
            data = get_auth_values(request)
            data.update({'success': False, 'm': u"متن پست الزامی است."})
            response = HttpResponse(json.dumps(data), 'application/json')
            return append_csrf(request, response)
    else:
        return initial_post(request)


def report_post(request, post_id):
    check_user(request)
    post = get_object_or_404(Post, id=post_id)
    data = get_auth_values(request)
    PostReport.objects.create(user_id=request.user.id, post=post)
    data.update({'success': True})
    return HttpResponse(json.dumps(data), 'application/json')


@login_required
def like_post(request, post_id):
    check_user(request)
    post = get_object_or_404(Post, id=post_id, active=True)

    try:
        l = PostLike.objects.get(user=request.user, post_id=post_id)
        l.delete()
        state = 'off'
    except PostLike.DoesNotExist:
        PostLike.objects.create(user=request.user, post_id=post_id)
        state = 'on'

    post.refresh_from_db()

    data = get_auth_values(request)
    data.update({'s': state, 'lc': post.like_count})
    return HttpResponse(json.dumps(data), 'application/json')


@login_required
def like_comment(request, comment_id):
    check_user(request)
    comment = get_object_or_404(Comment, id=comment_id)

    try:
        l = LikeComment.objects.get(user=request.user, comment_id=comment_id)
        l.delete()
        state = 'off'
    except LikeComment.DoesNotExist:
        LikeComment.objects.create(user=request.user, comment_id=comment_id)
        state = 'on'

    comment.refresh_from_db()

    data = get_auth_values(request)
    data.update({'s': state, 'lc': comment.like_count})
    return HttpResponse(json.dumps(data), 'application/json')


def post_page(request, post_id):
    check_user(request)
    post = get_object_or_404(Post, id=post_id, active=True)

    return HttpResponse(post.get_detail_json(request.user), 'application/json')


# def recommends(request):
#     wares = WareModel.objects.filter(active=True, recommends__isnull=False).select_subclasses().distinct()
#     return HttpResponse(WareModel.get_summery_json(handle_search(request, wares)), 'application/json')

# def populars(request):
#     wares = WareModel.objects.filter(active=True, populars__isnull=False).exclude(
#         WareModel.get_default_queryset()).select_subclasses().distinct()
#     return HttpResponse(WareModel.get_summery_json(handle_search(request, wares)), 'application/json')


@login_required
def set_fav(request, movie_id):
    check_user(request)
    try:
        movie = Post.objects.get(id=movie_id)
    except Post.DoesNotExist:
        raise Http404
    if Favorite.objects.is_favorite(request.user, movie):
        Favorite.objects.del_favorite(request.user, movie)
        message = u" %s با موفقیت از علاقه مندی ها حذف شد" % movie.name
        state = 'off'
    else:
        Favorite.objects.create_favorite(request.user, movie)
        message = u" %s با موفقیت به علاقه مندی ها اضافه شد" % movie.name
        state = 'on'
    data = get_auth_values(request)
    data.update({'m': message, 's': state})
    return HttpResponse(json.dumps([data]), 'application/json')


@login_required
def my_fav(request):
    check_user(request)
    fav_s = Favorite.objects.filter(
        user=request.user, )
    # ).distinct('object_id')
    fav_dict = []
    for fav in fav_s:
        obj = Post.objects.get(id=fav.object_id)
        fav_dict.append({'n': obj.name, "ty": obj._meta.verbose_name, 'co': obj.code,
                         'd': gregorian_to_jalali(fav.created_time.date()), 'i': obj.id})
    return HttpResponse(json.dumps(fav_dict), 'application/json')


@login_required
def my_comments(request):
    check_user(request)
    comments = Comment.objects.filter(
        user=request.user,
    )
    comments_dict = []
    for comment in comments:
        obj = Post.objects.get(id=comment.object_pk)
        comments_dict.append({'t': comment.user_name, 'c': comment.text,
                              's': comment.color,
                              'n': obj.name, 'i': obj.id,
                              "ty": obj._meta.verbose_name, 'co': obj.code,
                              'd': gregorian_to_jalali(comment.created_on)})
    return HttpResponse(json.dumps(comments_dict), 'application/json')


@login_required
def send_comment(request, post_id, comment_id=None):
    check_user(request)
    if request.method == 'POST':
        text = striptags(request.POST.get('text')).strip()
        comment = None
        if comment_id:
            comment = get_object_or_404(Comment, id=comment_id)
        if text:
            comment = Comment(
                content_type=PostContentType,
                object_pk=smart_text(post_id),
                text=striptags(text),
                user=request.user if request.user.is_authenticated() else None,
                user_name=request.user.username or "ناشناس",
                reply_to=comment
            )

            comment.save()
            data = get_auth_values(request)
            data.update({'success': True})

            comments = Comment.objects.filter(
                content_type=PostContentType,
                object_pk=smart_text(post_id),
                active=True
            )

            comments_arr = CommentHandler(comments, user_id=request.user.id).render_comments_json()
            data.update({'c': comments_arr})

            get_object_or_404(Post, id=post_id).update()

            return HttpResponse(json.dumps(data), 'application/json')
        else:
            data = get_auth_values(request)
            data.update({'success': False, 'm': u"متن نظر الزامی است."})
            response = HttpResponse(json.dumps(data), 'application/json')
            return append_csrf(request, response)
    else:
        return initial_post(request)


def send_suggestion(request):
    check_user(request)
    if request.method == 'POST':
        email = request.POST.get('email')
        title = request.POST.get('title')
        sug_type = request.POST.get('sug_type')
        print(sug_type)
        body = request.POST.get('body')
        phone = request.POST.get('phone')
        user = None
        if request.user.is_authenticated():
            user = request.user
        if title and body:
            suggestion = Suggestion(
                email=email,
                name=title,
                body=body,
                phone=phone,
                sug_type=sug_type,
                creator=user,
            )
            suggestion.save()
            data = get_auth_values(request)
            data.update({'success': True})
            return HttpResponse(json.dumps(data), 'application/json')
        else:
            data = get_auth_values(request)
            data.update({'success': False, 'm': u"لطفا فیلدهای ضروری را پر نمایید."})
            response = HttpResponse(json.dumps(data), 'application/json')
            return append_csrf(request, response)
    else:
        return initial_post(request)


def forget(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            if not Profile.objects.filter(email=email).exists():
                data = get_auth_values(request)
                data.update({'success': False, 'm': u"کاربری با این پست الکترونیک پیدا نشد."})
                response = HttpResponse(json.dumps(data), 'application/json')
                return append_csrf(request, response)
            else:
                MessageServices.send_forget_password(email)
                data = get_auth_values(request)
                data.update({'success': True})
                return HttpResponse(json.dumps(data), 'application/json')
        else:
            data = get_auth_values(request)
            data.update({'success': False, 'm': u"پست الکترونیک نامعتبر است."})
            response = HttpResponse(json.dumps(data), 'application/json')
            return append_csrf(request, response)
    else:
        return initial_post(request)


def posts(request):
    check_user(request)
    p = request.GET.get('p')

    posts_obj = Post.get_queryset_by_param(p).order_by('-id')[:5]

    return HttpResponse(Post.get_summery_json(posts_obj, request.user), 'application/json')


def last_posts(request, last_id):
    check_user(request)
    if not last_id or last_id == 0:
        last_id = 99999999

    p = request.GET.get('p')

    posts_obj = Post.get_queryset_by_param(p)

    posts_obj = posts_obj.filter(id__gt=last_id).order_by('-id')[:5]

    return HttpResponse(Post.get_summery_json(posts_obj, request.user), 'application/json')


def next_posts(request, first_id):
    check_user(request)
    if not first_id or first_id == -1:
        first_id = 0

    p = request.GET.get('p')

    posts_obj = Post.get_queryset_by_param(p)

    posts_obj = posts_obj.filter(id__lt=first_id).order_by('-id')[:5]

    return HttpResponse(Post.get_summery_json(posts_obj, request.user), 'application/json')


def page(request, post_id):
    check_user(request)
    post = get_object_or_404(Post, id=post_id, active=True)

    return HttpResponse(post.get_page_json(request.user), 'application/json')


def more_comment(request, post_id):
    check_user(request)

    first_id = request.GET.get('f')

    comments = Comment.objects.filter(
        content_type=PostContentType,
        object_pk=smart_text(post_id),
        active=True,
        id__gt=first_id
    ).order_by('-id')[:5]

    comments_arr = CommentHandler(comments, user_id=request.user.id).render_comments_json()
    data = {'c': comments_arr}

    return HttpResponse(json.dumps(data), 'application/json')


@login_required
def post_comment(request, post_id, comment_id=None):
    check_user(request)
    if request.method == 'POST':
        text = striptags(request.POST.get('text')).strip()
        comment = None
        if comment_id:
            comment = get_object_or_404(Comment, id=comment_id)
        if text:
            comment = Comment(
                content_type=PostContentType,
                object_pk=smart_text(post_id),
                text=striptags(text),
                user=request.user if request.user.is_authenticated() else None,
                user_name=request.user.username or "ناشناس",
                reply_to=comment
            )

            comment.save()
            data = get_auth_values(request)
            data.update({'success': True})

            comments = Comment.objects.filter(
                content_type=PostContentType,
                object_pk=smart_text(post_id),
                active=True
            ).order_by('-id')

            comments_arr = CommentHandler(comments, user_id=request.user.id).render_comments_json()
            data.update({'c': comments_arr})

            get_object_or_404(Post, id=post_id).update()

            return HttpResponse(json.dumps(data), 'application/json')
        else:
            data = get_auth_values(request)
            data.update({'success': False, 'm': u"متن نظر الزامی است."})
            response = HttpResponse(json.dumps(data), 'application/json')
            return append_csrf(request, response)
    else:
        return initial_post(request)


def users_page(request):
    check_user(request)
    p = request.GET.get('p')

    users_obj = Profile.get_queryset_by_param(p)[:20]

    res = []

    for user in users_obj:
        res.append(user.get_user_summery())

    return HttpResponse(json.dumps(res), 'application/json')


def fav_list_page(request):
    check_user(request)
    p = request.GET.get('p')

    posts_obj = Post.get_queryset_by_param(p)

    res = []

    for post in posts_obj:
        res.append(post.get_summery_fields())

    return HttpResponse(json.dumps(res), 'application/json')



def search_page(request):
    check_user(request)

    term = request.GET.get('t')
    post_type = request.GET.get('ty')
    first_id = request.GET.get('f')

    posts_obj = Post.objects.filter(active=True)

    if term:
        posts_obj = posts_obj.filter(text__icontains=term)

    if post_type:
        posts_obj = posts_obj.filter(post_type=post_type)

    if first_id:
        posts_obj = posts_obj.filter(id__lt=first_id)

    posts_obj = posts_obj.distinct().order_by('-id')[:5]

    data = []
    for post in posts_obj:
        data.append(post.get_summery_fields(request.user))

    res = {'d': data}

    return HttpResponse(json.dumps(res), 'application/json')


def user_search(request):
    check_user(request)

    term = request.GET.get('t')
    first_id = request.GET.get('f')

    users_obj = Profile.objects.filter()

    if term:
        users_obj = users_obj.filter(username__icontains=term)

    if first_id:
        users_obj = users_obj.filter(id__lt=first_id)

    users_obj = users_obj.distinct().order_by('-id')[:5]

    data = []
    for user in users_obj:
        data.append(user.get_user_summery())

    res = {'d': data}

    return HttpResponse(json.dumps(res), 'application/json')


def initial_post(request, **kwargs):
    data = get_auth_values(request)
    data.update(kwargs)
    response = HttpResponse(json.dumps(data), 'application/json')
    return append_csrf(request, response)


def get_auth_values(request):
    # print request.bill.get_android_fields()
    # print request.bill.payed
    if request.user.is_authenticated():
        return {'login': True, 'user': request.user.get_android_fields()}
    return {'login': False}


def append_csrf(request, response):
    from django.middleware.csrf import get_token

    csrf = get_token(request)
    response.set_cookie(key='csrf', value=csrf)
    return response


def check_user(request):
    if request.user.is_authenticated():
        # request.user.last_act = datetime.datetime.utcnow()
        request.user.save()


def app_info(request):
    data = {"v": settings.LAST_APP_VERSION, "s": settings.LAST_APP_SIZE, "c": settings.LAST_CHANGES,
            "l": settings.LAST_APP_LINK}
    return HttpResponse(json.dumps(data), 'application/json')
