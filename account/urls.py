# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url

__author__ = 'M.Y'

urlpatterns = patterns(
    'account.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^check/$', 'check', name='check'),
    url(r'^check_signup/$', 'check_signup', name='check_signup'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^signup/$', 'signup', name='signup'),
    url(r'^forget/$', 'forget', name='forget'),
    url(r'^change_pass/$', 'change_pass', name='change_pass'),
    url(r'^change_pass_ajax/$', 'change_pass_ajax', name='change_pass_ajax'),

)
