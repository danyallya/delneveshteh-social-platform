# -*- coding:utf-8 -*-


__author__ = 'M.Y'
from django import template

register = template.Library()

@register.filter
def is_like(post, user):
    return post.is_fav(user)
