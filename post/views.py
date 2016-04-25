import json

from django.db.models import Q
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.encoding import smart_text

from account.models import Profile
from android.views import check_user
from comment.models import Comment
from comment.views import send_comment_handler_view
from post.models import Post, PostContentType, PostLike


def base(request):
    return render(request, 'base.html', {})


def home(request, p='hot'):
    posts_obj = Post.get_queryset_by_param(p).order_by('-id')
    return render(request, 'home.html', {'posts': posts_obj, 'p': p})


def user_page(request, username):
    user = get_object_or_404(Profile, username=username)
    posts_obj = Post.objects.filter(active=True).filter(creator__username=username).order_by('-id')
    return render(request, 'home.html', {'posts': posts_obj})


def search_view(request):
    q = request.GET.get('q', '').strip()
    if q:
        posts_obj = Post.objects.filter(active=True). \
            filter(Q(creator__username__icontains=q) | Q(text__icontains=q)).order_by('-id')
    else:
        posts_obj = Post.objects.none()

    desc = 'جستجو برای: "%s"' % q
    return render(request, 'home.html', {'posts': posts_obj, 'desc': desc, 'q': q})


def post_page(request, post_id):
    post_obj = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(
        content_type=PostContentType,
        object_pk=smart_text(post_obj.id),
        active=True
    ).order_by('-id')

    return render(request, 'post.html', {'post': post_obj, 'comments': comments})


def like_ajax(request):
    check_user(request)

    post_id = request.POST.get('post_id')

    post = get_object_or_404(Post, id=post_id, active=True)

    try:
        l = PostLike.objects.get(user=request.user, post_id=post_id)
        l.delete()
        state = 'off'
    except PostLike.DoesNotExist:
        PostLike.objects.create(user=request.user, post_id=post_id)
        state = 'on'

    post.refresh_from_db()

    data = {'s': state, 'lc': post.like_count}
    return HttpResponse(json.dumps(data), 'application/json')


def send_comment(request):
    return send_comment_handler_view(request, PostContentType)
