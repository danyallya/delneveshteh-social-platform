# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url

__author__ = 'M.Y'

urlpatterns = patterns(
    'android.views',

    url(r'^initial_post/$', 'initial_post', name='android_initial_post'),
    url(r'^login/$', 'login', name='android_login'),
    url(r'^signup/$', 'signup', name='android_signup'),
    url(r'^edit_profile/$', 'edit_profile', name='android_edit_profile'),
    url(r'^logout/$', 'logout', name='android_logout'),
    url(r'^set_fav/(?P<movie_id>\d+)/$', 'set_fav', name='android_set_fav'),
    url(r'^posts/$', 'post_list', name='android_posts'),

    url(r'^post/(?P<post_id>\d+)/$', 'post_page', name='android_post_page'),

    url(r'^my_comments/$', 'my_comments', name='android_my_comments'),
    url(r'^my_fav/$', 'my_fav', name='android_my_fav'),
    url(r'^send_comment/(?P<movie_id>\d+)/$', 'send_comment', name='android_send_comment'),
    url(r'^send_suggestion/$', 'send_suggestion', name='android_send_suggestion'),
    url(r'^forget/$', 'forget', name='android_forget'),

)
