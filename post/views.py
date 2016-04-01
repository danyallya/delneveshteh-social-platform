from django.shortcuts import render, get_object_or_404
from django.utils.encoding import smart_text

from comment.models import Comment
from post.models import Post, PostContentType


def base(request):
    return render(request, 'base.html', {})


def home(request):
    posts = Post.objects.filter(active=True).order_by('-id')
    return render(request, 'home.html', {'posts': posts})


def post(request, post_id):
    post_obj = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(
        content_type=PostContentType,
        object_pk=smart_text(post_obj.id),
        active=True
    ).order_by('-id')

    return render(request, 'post.html', {'post': post_obj, 'comments': comments})
