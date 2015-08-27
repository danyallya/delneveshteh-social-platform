# -*- coding:utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe

__author__ = 'M.Y'


# def initial_dec(function):
#     def new_init(self, *args, **kwargs):
#         res = function(self, *args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs.update({'placeholder': self.fields[field].label})
#         return res
#
#     return new_init


class BaseForm(forms.ModelForm):
    has_provider = True

    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        if self.has_provider:
            self.provide_fields()

    def provide_fields(self):
        self.label_suffix = ''
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'placeholder': self.fields[field].label.replace(u":  <span class='red'>*</span>", '')})
            if self.fields[field].required and u"*" not in self.fields[field].label:
                self.fields[field].label += u":  <span class='red'>*</span>"
                self.fields[field].label = mark_safe(self.fields[field].label)

    def clean(self):
        cd = super(BaseForm, self).clean()
        for field in cd:
            if isinstance(cd[field], str):
                cd[field] = cd[field].strip()
        return cd
