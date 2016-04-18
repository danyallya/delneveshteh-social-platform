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
    url(r'^admin/', include(admin.site.urls)),  # admin site
    url(r'^account/', include('account.urls')),
    url(r'^android/', include('android.urls')),

    url(r'^base/$', 'post.views.base', name='base'),
    url(r'^$', 'post.views.home', name='home'),
    url(r'^post/(?P<post_id>\d+)/$', 'post.views.post_page', name='post_page'),
    url(r'^like_ajax/$', 'post.views.like_ajax', name='like_ajax'),
    url(r'^send_comment/$', 'post.views.send_comment', name='send_comment'),

]

urlpatterns += [
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
]
