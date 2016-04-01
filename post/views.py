import json

from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.encoding import smart_text

from android.views import check_user
from comment.models import Comment
from post.models import Post, PostContentType, PostLike


def base(request):
    return render(request, 'base.html', {})


def home(request):
    posts = Post.objects.filter(active=True).order_by('-id')
    return render(request, 'home.html', {'posts': posts})


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
