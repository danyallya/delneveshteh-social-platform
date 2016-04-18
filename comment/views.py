import json

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import striptags
from django.template.loader import render_to_string
from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe

from comment.models import Comment, LikeComment, ReportComment
from utils.persian import arToPersianChar


@login_required
def like_comment(request):
    comment_id = request.POST.get('id')
    comment = get_object_or_404(Comment, id=comment_id)
    try:
        l = LikeComment.objects.get(user=request.user, comment_id=comment_id)
        l.delete()
        state = 'off'
    except LikeComment.DoesNotExist:
        LikeComment.objects.create(user=request.user, comment_id=comment_id)
        state = 'on'

    comment.refresh_from_db()

    return HttpResponse(json.dumps({'c': comment.like_count, 'l': comment.is_liked(request.user)}),
                        'application/json')


def report_comment(request):
    comment_id = request.POST.get('id')
    comment = get_object_or_404(Comment, id=comment_id)
    # state = request.GET.get('state')
    # if state:
    ReportComment.objects.create(user=request.user, comment=comment, state=3)
    success = True

    return HttpResponse(json.dumps({'s': success}), 'application/json')


@login_required
def rm_comment(request):
    comment_id = request.POST.get('id')
    comment = get_object_or_404(Comment, id=comment_id)
    success = False
    if comment.user_id == request.user.id:
        comment.delete()
        success = True
    return HttpResponse(json.dumps({'s': success}), 'application/json')


def send_comment_handler_view(request, content_type):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(content_type.model_class().objects.get(id=request.POST.get('obj_id')).page_url)

    if request.method == 'POST':
        text = arToPersianChar(request.POST.get('text'))
        comment = request.POST.get('reply')
        obj_id = request.POST.get('obj_id')
        if text:
            comment = Comment(
                content_type=content_type,
                object_pk=smart_text(obj_id),
                text=striptags(text),
                user=request.user,
                user_name=request.user.username,
                reply_to_id=comment
            )
            comment.save()

            comment.mine = True

            content = render_to_string('comment_item.html', {'comment': comment, 'user': request.user})

            comment_count = comment.content_type.model_class().objects.get(id=comment.object_pk).comments_count

            return HttpResponse(json.dumps({'content': mark_safe(content), 'count': comment_count}), 'application/json')
