from django import template
from comment.handler import CommentHandler

register = template.Library()


@register.filter
def render_tree(comments):
    return CommentHandler(comments).render()


@register.filter
def render_tree_inline(comments):
    return CommentHandler(comments).render_comments_inline()
