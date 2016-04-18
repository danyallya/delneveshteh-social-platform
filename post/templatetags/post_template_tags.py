# -*- coding:utf-8 -*-
import re

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

__author__ = 'M.Y'

register = template.Library()


@register.filter
def is_like(post, user):
    return post.is_fav(user)


@register.filter
def max_str(val, size):
    if len(val) > size:
        return val[:size - 1] + " ..."
    else:
        return val


@register.filter
@stringfilter
def stripjs(value):
    stripped = re.sub(r'<script(?:\s[^>]*)?(>(?:.(?!/script>))*</script>|/>)',
                      '', str(value), flags=re.S)
    return mark_safe(stripped)
