"""fanoos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^adminoo/', include(admin.site.urls)),  # admin site
    url(r'^account/', include('account.urls')),
    url(r'^android/', include('android.urls')),

]

urlpatterns += [
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
]

urlpatterns += [
    url(r'^$', 'post.views.home', name='home', kwargs={'p': 'hot'}),
    url(r'^del/$', 'post.views.home', name='del', kwargs={'p': 'del'}),
    url(r'^discuss/$', 'post.views.home', name='talk', kwargs={'p': 'talk'}),
    url(r'^say/$', 'post.views.home', name='hadis', kwargs={'p': 'hadis'}),
    url(r'^event/$', 'post.views.home', name='monasebat', kwargs={'p': 'monasebat'}),

    url(r'^search/$', 'post.views.search_view', name='search'),

    url(r'^post/(?P<post_id>\d+)/$', 'post.views.post_page', name='post_page'),
    url(r'^like_ajax/$', 'post.views.like_ajax', name='like_ajax'),
    url(r'^send_comment/$', 'post.views.send_comment', name='send_comment'),

    url(r'^(?P<username>\w+)/$', 'post.views.user_page', name='user_page'),

]
