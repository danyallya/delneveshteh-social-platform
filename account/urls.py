# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url

__author__ = 'M.Y'

urlpatterns = patterns(
    'account.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^signup/$', 'signup', name='signup'),
    url(r'^forget/$', 'forget', name='forget'),
    url(r'^edit_profile/$', 'edit_profile', name='edit_profile'),
    url(r'^search/$', 'search', name='search'),
    url(r'^search_ajax/$', 'search_ajax', name='search_ajax'),

)
