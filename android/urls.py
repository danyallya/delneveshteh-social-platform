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
    url(r'^posts/(?P<last_id>\d+)/$', 'last_post_list', name='android_last_post_list'),
    url(r'^next_posts/(?P<first_id>\d+)/$', 'next_post_list', name='android_next_post_list'),

    url(r'^user_posts/(?P<username>\w+)/$', 'user_post_list', name='android_user_posts'),
    url(r'^user_posts/(?P<username>\w+)/(?P<last_id>\d+)/$', 'user_last_post_list', name='android_user_last_post_list'),
    url(r'^user_next_posts/(?P<username>\w+)/(?P<first_id>\d+)/$', 'user_next_post_list', name='android_user_next_post_list'),

    url(r'^last_post_count/(?P<last_id>\d+)/$', 'last_post_count', name='android_last_post_count'),

    url(r'^send_post/$', 'send_post', name='android_send_post'),

    url(r'^report_post/(?P<post_id>\d+)/$', 'report_post', name='android_report_post'),
    url(r'^like_post/(?P<post_id>\d+)/$', 'like_post', name='android_like_post'),
    url(r'^like_comment/(?P<comment_id>\d+)/$', 'like_comment', name='android_like_comment'),

    url(r'^post/(?P<post_id>\d+)/$', 'post_page', name='android_post_page'),

    url(r'^my_comments/$', 'my_comments', name='android_my_comments'),
    url(r'^my_fav/$', 'my_fav', name='android_my_fav'),
    url(r'^send_comment/(?P<post_id>\d+)/$', 'send_comment', name='android_send_comment'),
    url(r'^send_suggestion/$', 'send_suggestion', name='android_send_suggestion'),
    url(r'^forget/$', 'forget', name='android_forget'),

    url(r'^app_info/$', 'app_info', name='android_app_info'),

)
