# -*- coding: utf-8 -*-
import datetime
from utils.calverter import gregorian_to_jalali

from django import template

register = template.Library()


@register.filter
def pdate_if_date(value):
    if isinstance(value, datetime.date):
        return gregorian_to_jalali(value)
    if value is None or value == 'None' or value == '':
        return '---'
    return value
